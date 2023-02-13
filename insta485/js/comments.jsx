import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
export default function Comments({ url, comments }) {
  const [formText, setFormText] = useState("");
  const [commentList, setCommentList] = useState([...comments]);

  var postid = url.replace("/api/v1/posts/", "");
  postid = postid.replace("/", "");
  url = "/api/v1/comments/?postid=" + postid;

  function handleDelete(event) {
    console.log(event);
    var id_to_delete = event.target.id;
    var url_delete = "/api/v1/comments/" + id_to_delete + "/";
    event.preventDefault();
    let ignoreStaleRequest = false;
    fetch(url_delete, {
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setCommentList([...commentList, ...[data]]);
        }
      })
      .catch((error) => console.log(error));
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    let ignoreStaleRequest = false;
    fetch(url, {
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ text: formText }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setCommentList([...commentList, ...[data]]);
        }
      })
      .catch((error) => console.log(error));
    setFormText("");
  };

  const handleChange = (event) => {
    event.preventDefault();
    setFormText(event.target.value);
  };
  return (
    <div>
      {comments.map((comment) => {
        // Return HTML for one clue
        if (comment["lognameOwnsThis"]) {
          return (
            <div>
              {comment["owner"]} {comment["text"]}
              <button onClick={handleDelete} id={comment["commentid"]}>
                delete
              </button>
            </div>
          );
        }
        return (
          <div>
            {comment["owner"]} {comment["text"]}
          </div>
        );
      })}
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
