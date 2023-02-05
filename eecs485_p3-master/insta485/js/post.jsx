import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Likes from './likes';
import Comments from './comments';

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      age: '',
      img_url: '',
      owner: '',
      owner_img_url: '',
      owner_show_url: '',
      post_show_url: '',
      url: '',
      like_url: '',
      comment_url: '',
    };
  }

  componentDidMount() {
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          age: moment.utc(data.age).local().fromNow(),
          img_url: data.img_url,
          owner: data.owner,
          owner_img_url: data.owner_img_url,
          owner_show_url: data.owner_show_url,
          post_show_url: data.post_show_url,
          url: data.url,
          like_url: `${data.url}likes/`,
          comment_url: `${data.url}comments/`,
        });
        console.log(this.state.like_url);
        console.log(this.state.comment_url);
      })
      .catch((error) => console.log(error)); // eslint-disable-line no-console
  }

  render() {
    return (
      <div className='post'>
        <a href={this.state.owner_show_url}>
          <p>
            <img
              src={this.state.owner_img_url}
              alt='whatev'
            />
          </p>
        </a>
        <a href={this.state.owner_show_url}>
          <p>{this.state.owner}</p>
        </a>
        <a href={this.state.post_show_url}>
          <p>{this.state.age}</p>
        </a>
        <p>
          <img
            src={this.state.img_url}
            alt='whatev'
          />
        </p>
        <Likes url={`${this.props.url}likes/`} />
        <Comments url={`${this.props.url}comments/`} />
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
