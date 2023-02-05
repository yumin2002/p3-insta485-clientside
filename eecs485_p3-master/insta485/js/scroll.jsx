import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import PropTypes from 'prop-types';

import Post from './post';

class Scroll extends React.Component {
  constructor(props) {
    // Initialize mutable state
    // always call super when defining the constructor of a subclass
    super(props);
    this.state = { next: '', history_log: [] };
    this.backButton = this.backButton.bind(this);

    if (performance.navigation.type === 2) {
      this.backButton(history.state);
    }

    this.fetchMoreData = () => {
      //    console.log("fetch more data...");
      //    console.log(this.state);
      if (this.state.next === '') {
        return;
      }
      this.update(this.state.next);
    };
  }

  // fetch data
  componentDidMount() {
    if (PerformanceNavigation.type === 2) {
      this.backButton(history.state);
    } else {
      this.update(this.props.url);
    }
  }

  update(apiUrl) {
    fetch(apiUrl, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          next: data.next,
          history_log: this.state.history_log.concat(data.results),
        });
        history.replaceState(
          { next: this.state.next, history_log: this.state.history_log },
          '',
          ''
        );
      })
      .catch((error) => console.log(error));
  }

  backButton(state) {
    this.state.next = state.next;
    this.state.history_log = state.history_log;
  }

  render() {
    return (
      <div>
        <hr />

        <InfiniteScroll
          dataLength={this.state.history_log.length}
          next={this.fetchMoreData}
          hasMore
          loader={<h4>Loading...</h4>}
        >
          {this.state.history_log.map((result) => (
            <Post url={result.url} />
          ))}
        </InfiniteScroll>
      </div>
    );
  }
}

Scroll.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Scroll;
