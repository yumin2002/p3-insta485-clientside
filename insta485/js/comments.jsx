import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
export default function Comments({ handleSubmit, handleDelete, comments }) {
  return (
    <div>
      {comments.map((comment) => {
        // Return HTML for one clue
        if (comment["lognameOwnsThis"]) {
          return (
            <div key={comments["commentid"]}>

              {comment["owner"]} {comment["text"]}
              <button onClick={handleDelete} id={comment["commentid"]} key={comments["commentid"]}>
                delete
              </button>
            </div>
          );
        }
        return (
          <div key={comments["commentid"]}>
            {comment["owner"]} {comment["text"]}
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
