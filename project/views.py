import re
import time
import logging
from typing import NamedTuple, List, Dict, Any, Optional
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import SafeString
from django.utils import translation
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from project.util import django_graphql_forms
from project.justfix_environment import BASE_DIR
from project.util.lambda_pool import LambdaPool
from project.schema import schema
from project import common_data
import project.health

# This is changed by test suites to ensure that
# everything works okay when the server-side renderer fails
# (relatively) gracefully.
TEST_INTERNAL_SERVER_ERROR = False

FRONTEND_QUERY_DIR = BASE_DIR / 'frontend' / 'lib' / 'queries' / 'autogen'

FORMS_COMMON_DATA = common_data.load_json("forms.json")

NS_PER_MS = 1e+6

logger = logging.getLogger(__name__)

lambda_pool = LambdaPool(
    'React',
    BASE_DIR / 'lambda.js',
    cwd=BASE_DIR,
    restart_on_script_change=settings.DEBUG
)


class GraphQLQueryPrefetchInfo(NamedTuple):
    '''
    Encapsulates details from the server-side renderer
    about a GraphQL query that should (ideally) be
    pre-fetched for the current request.
    '''

    graphql: str
    input: Any


class LambdaResponse(NamedTuple):
    '''
    Encapsulates the result of the server-side renderer.

    This is more or less the same as the LambdaResponse
    interface defined in frontend/lambda/lambda.tsx.
    '''

    html: SafeString
    title_tag: SafeString
    meta_tags: SafeString
    status: int
    bundle_files: List[str]
    modal_html: SafeString
    location: Optional[str]
    traceback: Optional[str]
    graphql_query_to_prefetch: Optional[GraphQLQueryPrefetchInfo]

    # The amount of time rendering took, in milliseconds.
    render_time: int


def find_all_graphql_fragments(query: str) -> List[str]:
    '''
    >>> find_all_graphql_fragments('blah')
    []
    >>> find_all_graphql_fragments('query { ...Thing,\\n ...OtherThing }')
    ['Thing', 'OtherThing']
    '''

    results = re.findall(r'\.\.\.([A-Za-z0-9_]+)', query)
    return [thing for thing in results]


def add_graphql_fragments(query: str) -> str:
    all_graphql = [query]
    to_find = find_all_graphql_fragments(query)

    while to_find:
        fragname = to_find.pop()
        fragpath = FRONTEND_QUERY_DIR / f"{fragname}.graphql"
        fragtext = fragpath.read_text()
        to_find.extend(find_all_graphql_fragments(fragtext))
        all_graphql.append(fragtext)

    return '\n'.join(all_graphql)


def run_react_lambda(initial_props) -> LambdaResponse:
    start_time = time.time_ns()
    response = lambda_pool.run_handler(initial_props)
    render_time = int((time.time_ns() - start_time) / NS_PER_MS)

    pf = response['graphQLQueryToPrefetch']
    if pf is not None:
        pf = GraphQLQueryPrefetchInfo(
            graphql=pf['graphQL'],
            input=pf['input']
        )

    return LambdaResponse(
        html=SafeString(response['html']),
        modal_html=SafeString(response['modalHtml']),
        title_tag=SafeString(response['titleTag']),
        meta_tags=SafeString(response['metaTags']),
        status=response['status'],
        bundle_files=response['bundleFiles'],
        location=response['location'],
        traceback=response['traceback'],
        graphql_query_to_prefetch=pf,
        render_time=render_time
    )


def execute_query(request, query: str, variables=None) -> Dict[str, Any]:
    result = schema.execute(query, context=request, variables=variables)
    if result.errors:
        raise Exception(result.errors)
    return result.data


def get_initial_session(request) -> Dict[str, Any]:
    data = execute_query(
        request,
        add_graphql_fragments('''
        query GetInitialSession {
            session {
                ...AllSessionInfo
            }
        }
        ''')
    )
    return data['session']


class LegacyFormSubmissionError(Exception):
    pass


def fix_newlines(d: Dict[str, str]) -> Dict[str, str]:
    result = dict()
    result.update(d)
    for key in d:
        result[key] = result[key].replace('\r\n', '\n')
    return result


def get_legacy_form_submission_result(request, graphql, input):
    if request.POST.get(FORMS_COMMON_DATA["LEGACY_FORMSET_ADD_BUTTON_NAME"]):
        return None
    return execute_query(request, graphql, variables={'input': input})['output']


def get_legacy_form_submission(request):
    graphql = request.POST.get('graphql')

    if not graphql:
        raise LegacyFormSubmissionError('No GraphQL query found')

    input_type = django_graphql_forms.get_input_type_from_query(graphql)

    if not input_type:
        raise LegacyFormSubmissionError('Invalid GraphQL query')

    form_class = django_graphql_forms.get_form_class_for_input_type(input_type)

    if not form_class:
        raise LegacyFormSubmissionError('Invalid GraphQL input type')

    formset_classes = django_graphql_forms.get_formset_classes_for_input_type(input_type)
    exclude_fields = django_graphql_forms.get_exclude_fields_for_input_type(input_type)

    input = django_graphql_forms.convert_post_data_to_input(
        form_class, request.POST, formset_classes, exclude_fields)

    return {
        'input': input,
        'result': get_legacy_form_submission_result(request, graphql, input),
        'POST': fix_newlines(request.POST.dict())
    }


def react_rendered_view(request):
    url = request.path
    cur_language = ''
    if settings.USE_I18N:
        cur_language = translation.get_language_from_request(request, check_path=True)
    querystring = request.GET.urlencode()
    if querystring:
        url += f'?{querystring}'
    webpack_public_path_url = f'{settings.STATIC_URL}frontend/'

    initial_props: Dict[str, Any] = {}

    if request.method == "POST":
        try:
            # It's important that we process the legacy form submission
            # *before* getting the initial session, so that when we
            # get the initial session, it reflects any state changes
            # made by the form submission. This will ensure the same
            # behavior between baseline (non-JS) and progressively
            # enhanced (JS) clients.
            legacy_form_submission = get_legacy_form_submission(request)
        except LegacyFormSubmissionError as e:
            return HttpResponseBadRequest(e.args[0])
        initial_props['legacyFormSubmission'] = legacy_form_submission

    # Currently, the schema for this structure needs to be mirrored
    # in the AppProps interface in frontend/lib/app.tsx. So if you
    # add or remove anything here, make sure to do the same over there!
    initial_props.update({
        'initialURL': url,
        'initialSession': get_initial_session(request),
        'locale': cur_language,
        'server': {
            'originURL': request.build_absolute_uri('/')[:-1],
            'staticURL': settings.STATIC_URL,
            'webpackPublicPathURL': webpack_public_path_url,
            'adminIndexURL': reverse('admin:index'),
            'batchGraphQLURL': reverse('batch-graphql'),
            'locHtmlURL': reverse('loc', args=('html',)),
            'locPdfURL': reverse('loc', args=('pdf',)),
            'redirectToLegacyAppURL': reverse('redirect-to-legacy-app'),
            'debug': settings.DEBUG
        },
        'testInternalServerError': TEST_INTERNAL_SERVER_ERROR,
    })

    lambda_response = run_react_lambda(initial_props)
    render_time = lambda_response.render_time

    if lambda_response.status == 200 and lambda_response.graphql_query_to_prefetch:
        # The page rendered, but it has a "loading..." message somewhere on it
        # that's waiting for a GraphQL request to complete. Let's pre-fetch that
        # request and re-render the page, so that the user receives it without
        # any such messages (and so the user can see all the content if their
        # JS isn't working).
        pfquery = lambda_response.graphql_query_to_prefetch
        initial_props['server']['prefetchedGraphQLQueryResponse'] = {
            'graphQL': pfquery.graphql,
            'input': pfquery.input,
            'output': execute_query(request, pfquery.graphql, pfquery.input)
        }
        lambda_response = run_react_lambda(initial_props)
        render_time += lambda_response.render_time

    bundle_files = lambda_response.bundle_files
    bundle_urls = [
        f'{webpack_public_path_url}{bundle_file}'
        for bundle_file in bundle_files
    ]
    if lambda_response.status == 500:
        # It's a 500 error page, don't include any client-side JS.
        bundle_urls = []
        logger.error(lambda_response.traceback)
    elif lambda_response.status == 302 and lambda_response.location:
        return redirect(to=lambda_response.location)

    logger.debug(f"Rendering {url} in Node.js took {render_time} ms.")

    return render(request, 'index.html', {
        'initial_render': lambda_response.html,
        'modal_html': lambda_response.modal_html,
        'title_tag': lambda_response.title_tag,
        'meta_tags': lambda_response.meta_tags,
        'bundle_urls': bundle_urls,
        'initial_props': initial_props,
    }, status=lambda_response.status)


@csrf_exempt
@require_POST
def example_server_error(request, id: str):
    '''
    This endpoint can be used to test integration with whatever
    error reporting system is configured.
    '''

    logger.error(
        f"This is an example server error log message with id '{id}'. "
        f"If you can read this, it means errors from the logging system "
        f"are being reported properly."
    )
    raise Exception(
        f"This is an example server exception with id '{id}'. "
        f"If you can read this, it means unexpected internal server "
        f"errors are being reported properly."
    )


def redirect_favicon(request):
    return redirect(f'{settings.STATIC_URL}favicon.ico')


def health(request):
    return project.health.check().to_json_response()
