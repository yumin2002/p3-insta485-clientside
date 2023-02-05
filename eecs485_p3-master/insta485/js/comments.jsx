import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '', comments: [] };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
        });
      })
      .catch((error) => console.log(error));
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch(this.props.url, {
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ text: this.state.value }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => ({
          comments: prevState.comments.concat([data]),
          value: '',
        }));
      })
      .catch((error) => console.log(error));
  }

  render() {
    return (
      <div>
        {this.state.comments.map((comment) => (
          <div key={comment.owner_show_url}>
            <a href={comment.owner_show_url}>{comment.owner}</a> {comment.text}
          </div>
        ))}
        <form
          id='comment-form'
          onSubmit={this.handleSubmit}
        >
          <input
            type='text'
            value={this.state.value}
            onChange={this.handleChange}
          />
        </form>
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
