import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes a like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { num_likes: 0, logname_likes_this: false };
    // fetch(this.props.url, { credentials: 'same-origin' })
    //   .then((response) => {
    //     if (!response.ok) throw Error(response.statusText);
    //     return response.json();
    //   })
    //   .then((data) => {
    //     this.state = { num_likes: data.likes_count,
    //       logname_likes_this: data.logname_likes_this };
    //   })
    //   .catch(error => console.log(error));
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          num_likes: data.likes_count,
          logname_likes_this: data.logname_likes_this,
        });
      })
      .catch((error) => console.log(error)); // eslint-disable-line no-console
  }

  componentWillReceiveProps(next) {
    this.props = next;
    fetch(next.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          num_likes: data.likes_count,
          logname_likes_this: data.logname_likes_this,
        });
      })
      .catch((error) => console.log(error)); // eslint-disable-line no-console
  }

  handleClick() {
    console.log('Hey');
    console.log('changed');
    fetch(
      this.props.url,
      {
        credentials: 'same-origin',
        method: this.state.logname_likes_this === false ? 'post' : 'delete',
      },
      console.log(this.state.logname_likes_this)
    )
      .then(() => {
        this.setState({
          logname_likes_this: !this.state.logname_likes_this,
          num_likes:
            this.state.logname_likes_this === true
              ? this.state.num_likes - 1
              : this.state.num_likes + 1,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // Render number of likes
    return (
      <div className='likes'>
        <p>{`${this.state.num_likes} like${
          this.state.num_likes !== 1 ? 's' : ''
        }`}</p>
        <button
          id='like-unlike-button'
          onClick={this.handleClick}
        >
          {this.state.logname_likes_this === true ? 'unlike' : 'like'}
        </button>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
