from graphql import ResolveInfo
from django.forms import ModelForm

from project.util.session_mutation import SessionFormMutation


def get_model_for_user(model_class, user):
    '''
    Given a model class that has a OneToOneField called 'user'
    that maps to a user, returns the model instance for the
    given user.

    If no such model exists, or if the user is not logged in,
    returns None.
    '''

    if not user.is_authenticated:
        return None
    try:
        return model_class.objects.get(user=user)
    except model_class.DoesNotExist:
        return None


def create_model_for_user_resolver(model_class):
    '''
    Creates a GraphQL resolver that returns the model instance
    associated with a given user.
    '''

    def resolver(parent, info: ResolveInfo):
        return get_model_for_user(model_class, info.context.user)

    return resolver


class OneToOneUserModelFormMutation(SessionFormMutation):
    '''
    A base class that can be used to make any
    ModelForm that represents a one-to-one relationship
    with the user into a GraphQL mutation.
    '''

    class Meta:
        abstract = True

    login_required = True

    @classmethod
    def get_form_kwargs(cls, root, info: ResolveInfo, **input):
        '''
        Either create a new instance of our model, or get the
        existing one, and pass it on to the ModelForm.
        '''

        user = info.context.user
        model = cls._meta.form_class._meta.model
        try:
            instance = model.objects.get(user=user)
        except model.DoesNotExist:
            instance = model(user=user)
        return {"data": input, "instance": instance}

    @classmethod
    def perform_mutate(cls, form: ModelForm, info: ResolveInfo):
        '''
        Save the ModelForm, which will have already been populated with
        an instance of our model.
        '''

        form.save()
        return cls.mutation_success()

    @classmethod
    def resolve(cls, parent, info: ResolveInfo):
        '''
        This can be used as a GraphQL resolver to get the
        related model instance for the current user.
        '''

        return get_model_for_user(cls._meta.form_class._meta.model, info.context.user)
