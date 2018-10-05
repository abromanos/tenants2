import React from 'react';
import Downshift, { ControllerStateAndHelpers, DownshiftInterface } from 'downshift';
import classnames from 'classnames';
import autobind from 'autobind-decorator';
import { BoroughChoice, getBoroughLabel } from './boroughs';
import { WithFormFieldErrors, formatErrors } from './form-errors';
import { bulmaClasses } from './bulma';
import { awesomeFetch, createAbortController } from './fetch';
import { renderLabel, LabelRenderer } from './form-fields';

/**
 * The keys here were obtained experimentally, I'm not actually sure
 * if/where they are formally specified.
 */
const BOROUGH_GID_TO_CHOICE: { [key: string]: BoroughChoice|undefined } = {
  'whosonfirst:borough:1': BoroughChoice.MANHATTAN,
  'whosonfirst:borough:2': BoroughChoice.BRONX,
  'whosonfirst:borough:3': BoroughChoice.BROOKLYN,
  'whosonfirst:borough:4': BoroughChoice.QUEENS,
  'whosonfirst:borough:5': BoroughChoice.STATEN_ISLAND,
};

export interface GeoAutocompleteItem {
  address: string;
  borough: BoroughChoice | null;
};

interface GeoAutocompleteProps extends WithFormFieldErrors {
  label: string;
  renderLabel?: LabelRenderer;
  initialValue?: GeoAutocompleteItem;
  onChange: (item: GeoAutocompleteItem) => void;
  onNetworkError: (err: Error) => void;
};

interface GeoSearchProperties {
  /** e.g. "Brooklyn" */
  borough: string;

  /** e.g. "whosonfirst:borough:2" */
  borough_gid: string;

  /** e.g. "150" */
  housenumber: string;

  /** e.g. "150 COURT STREET" */
  name: string;

  /** e.g. "150 COURT STREET, Brooklyn, New York, NY, USA" */
  label: string;
}

interface GeoSearchResults {
  bbox: unknown;
  features: {
    geometry: unknown;
    properties: GeoSearchProperties
  }[];
}

interface GeoAutocompleteState {
  isLoading: boolean;
  results: GeoAutocompleteItem[];
}

/**
 * The amount of ms we'll wait after the user pressed a key
 * before we'll issue a network request to fetch autocompletion
 * results.
 */
const AUTOCOMPLETE_KEY_THROTTLE_MS = 250;

/**
 * For documentation about this endpoint, see:
 * 
 * https://geosearch.planninglabs.nyc/docs/#autocomplete
 */
const GEO_AUTOCOMPLETE_URL = 'https://geosearch.planninglabs.nyc/v1/autocomplete';

/** The maximum number of autocomplete suggestions to show. */
const MAX_SUGGESTIONS = 5;

/**
 * An address autocomplete field. This should only be used as a
 * progressive enhancement, since it requires JavaScript and uses
 * a third-party API that might become unavailable.
 */
export class GeoAutocomplete extends React.Component<GeoAutocompleteProps, GeoAutocompleteState> {
  keyThrottleTimeout: number|null;
  abortController?: AbortController;
  requestId: number;

  constructor(props: GeoAutocompleteProps) {
    super(props);
    this.state = {
      isLoading: false,
      results: []
    };
    this.requestId = 0;
    this.keyThrottleTimeout = null;
    this.abortController = createAbortController();
  }

  renderListItem(ds: ControllerStateAndHelpers<GeoAutocompleteItem>,
                 item: GeoAutocompleteItem,
                 index: number): JSX.Element {
    const props = ds.getItemProps({
      key: item.address + item.borough,
      index,
      item,
      className: classnames({
        'jf-autocomplete-is-highlighted': ds.highlightedIndex === index,
        'jf-autocomplete-is-selected': ds.selectedItem === item
      })
    });

    return (
      <li {...props}>
        {geoAutocompleteItemToString(item)}
      </li>
    );
  }

  getInputProps(ds: ControllerStateAndHelpers<GeoAutocompleteItem>) {
    const { results } = this.state;
    const selectFirstResult = (): boolean => {
      if (ds.highlightedIndex === null && ds.isOpen && results.length > 0) {
        ds.selectItem(results[0]);
        return true;
      }
      if (!ds.selectedItem || geoAutocompleteItemToString(ds.selectedItem) !== ds.inputValue) {
        ds.selectItem({
          address: ds.inputValue || '',
          borough: null
        });
      }
      return false;
    };
    return ds.getInputProps({
      onBlur: selectFirstResult,
      onKeyDown(event) {
        if ((event.keyCode === 13 || event.keyCode === 9) && selectFirstResult()) {
          event.preventDefault();
        }
      }
    });
  }

  renderAutocomplete(ds: ControllerStateAndHelpers<GeoAutocompleteItem>): JSX.Element {
    const { errorHelp } = formatErrors(this.props);
    const { results } = this.state;

    return (
      <div className="field jf-autocomplete-field">
        {renderLabel(this.props.label, ds.getLabelProps(), this.props.renderLabel)}
        <div className={bulmaClasses('control', {
          'is-loading': this.state.isLoading
        })}>
          <input className="input" {...this.getInputProps(ds)} />
          <ul className={classnames({
            'jf-autocomplete-open': ds.isOpen && results.length > 0
          })} {...ds.getMenuProps()}>
            {ds.isOpen && results.map((item, i) => this.renderListItem(ds, item, i))}
          </ul>
        </div>
        {errorHelp}
      </div>
    );
  }

  resetSearchRequest() {
    if (this.keyThrottleTimeout !== null) {
      window.clearTimeout(this.keyThrottleTimeout);
      this.keyThrottleTimeout = null;
    }
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = createAbortController();
    }
    this.requestId++;
  }

  @autobind
  handleFetchError(e: Error) {
    if (e instanceof DOMException && e.name === 'AbortError') {
      // Don't worry about it, the user just aborted the request.
    } else {
      // TODO: It would be nice if we could further differentiate
      // between a "you aren't connected to the internet"
      // error versus a "you issued a bad request" error, so that
      // we could report the error if it's the latter.
      this.props.onNetworkError(e);
    }
  }

  async fetchResults(value: string): Promise<void> {
    const originalRequestId = this.requestId;
    const url = `${GEO_AUTOCOMPLETE_URL}?text=${encodeURIComponent(value)}`;
    const res = await awesomeFetch(url, {
      signal: this.abortController && this.abortController.signal
    });
    const results = await res.json();
    if (this.requestId === originalRequestId) {
      this.setState({
        isLoading: false,
        results: geoSearchResultsToAutocompleteItems(results)
      });
    }
  }

  @autobind
  handleInputValueChange(value: string) {
    this.resetSearchRequest();
    if (value.length > 3 && value.indexOf(' ') > 0) {
      this.setState({ isLoading: true });
      this.keyThrottleTimeout = window.setTimeout(() => {
        this.fetchResults(value).catch(this.handleFetchError);
      }, AUTOCOMPLETE_KEY_THROTTLE_MS);
    } else {
      this.setState({ results: [], isLoading: false });
    }
  }

  componentWillUnmount() {
    this.resetSearchRequest();
  }

  render() {
    const GeoAutocomplete = Downshift as DownshiftInterface<GeoAutocompleteItem>;

    return (
      <GeoAutocomplete
        onChange={this.props.onChange}
        onInputValueChange={this.handleInputValueChange}
        defaultSelectedItem={this.props.initialValue}
        itemToString={geoAutocompleteItemToString}
      >
        {(downshift) => this.renderAutocomplete(downshift)}
      </GeoAutocomplete>
    );
  }
}

export function geoAutocompleteItemToString(item: GeoAutocompleteItem|null): string {
  if (!item) return '';
  if (!item.borough) return item.address;
  return `${item.address}, ${getBoroughLabel(item.borough)}`;
}

export function geoSearchResultsToAutocompleteItems(results: GeoSearchResults): GeoAutocompleteItem[] {
  return results.features.slice(0, MAX_SUGGESTIONS).map(feature => {
    const { borough_gid } = feature.properties;
    const borough = BOROUGH_GID_TO_CHOICE[borough_gid];

    if (!borough) {
      throw new Error(`No borough found for ${borough_gid}!`);
    }

    return {
      address: feature.properties.name,
      borough
    }
  });
}
