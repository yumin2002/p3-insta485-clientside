import React from "react";  // , { useState, useEffect } 
import PropTypes from "prop-types";

export default function Comments({ handleSubmit, handleDelete, comments }) {
  return (
    <div>
      {comments.map((comment) => {
        // Return HTML for one clue
        if (comment.get("lognameOwnsThis")) {
          //setuniqueid(uniqueid + 1)
          return (
            <div key={comment.get("commentid")}>
              <a href={comment.get("ownerShowUrl")}> {comment.get("owner")}</a>
              <span className="comment-text">{comment.get("text")}</span>
              <button
                type="button"
                className="delete-comment-button"
                onClick={handleDelete}
                id={comment.get("commentid")}
              >
                delete
              </button>
            </div>
          );
        }
        return (
          <div key={comment.get("commentid")}>
            <a href={comment.get("ownerShowUrl")}> {comment.get("owner")}</a>
            <span className="comment-text">{comment.get("text")}</span>
          </div>
        );
      })}
      <form className="comment-form" onSubmit={handleSubmit}>
        <input type="text" />
      </form>
    </div>
  );
}
Comments.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  handleDelete: PropTypes.func.isRequired,
  comments: PropTypes.array.isRequired,
};
