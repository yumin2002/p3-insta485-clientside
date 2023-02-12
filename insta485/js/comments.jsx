import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
export default function Comments({ url, comments }) {
  const [formText, setFormText] = useState("");
  const [commentList, setCommentList] = useState([]);

  var postid = url.replace("/api/v1/posts/", "");
  url = "/api/v1/comments/?postid=" + postid;
  console.log(url);

  const renderedComments = comments.map((comment) => {
    // Return HTML for one clue
    if (comment["lognameOwnsThis"]) {
      return (
        <div>
          {comment["owner"]} {comment["text"]}
          <button onClick={handleDelete}>delete</button>
        </div>
      );
    }
    return (
      <div>
        {comment["owner"]} {comment["text"]}
      </div>
    );
  });
  const handleDelete = (event) => {};

  const handleSubmit = (event) => {
    let ignoreStaleRequest = false;
    fetch(url, { credentials: "same-origin", method: "POST" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
        }
      })
      .catch((error) => console.log(error));
    event.preventDefault();
    setFormText("");
  };

  const handleChange = (event) => {
    event.preventDefault();
    setFormText(event.target.value);
  };
  return (
    <div>
      {renderedComments}
      <form id="comment-form">
        <input
          id="input"
          type="text"
          onChange={handleChange}
          value={formText}
        />
        <button id="submit" onClick={handleSubmit}>
          comment
        </button>
      </form>
    </div>
  );
}
Comments.propTypes = {
  url: PropTypes.string.isRequired,
  comments: PropTypes.array.isRequired,
};
