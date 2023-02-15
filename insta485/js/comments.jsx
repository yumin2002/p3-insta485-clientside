import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
export default function Comments({ handleSubmit, handleDelete, comments }) {
  return (
    <div>
      {comments.map((comment) => {

        // Return HTML for one clue
        if (comment["lognameOwnsThis"]) {
          //setuniqueid(uniqueid + 1)
          return (
            <div key={comment["commentid"]}>
              <a href={comment["ownerShowUrl"]}> {comment["owner"]}</a>
              {comment["text"]}
              <button onClick={handleDelete} id={comment["commentid"]}>
                delete
              </button>

            </div>

          );

        }
        return (
          <div key={comment["commentid"]}>
            <a href={comment["ownerShowUrl"]}> {comment["owner"]}</a> {comment["text"]}
          </div>
        );

      })}
      <form className="comment-form" onSubmit={handleSubmit}>
        <input type="text" />
      </form>
    </div >
  );
}
Comments.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  handleDelete: PropTypes.func.isRequired,
  comments: PropTypes.array.isRequired,
};
