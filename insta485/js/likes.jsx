import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
export default function UpdateLikes({
  btext,
  num,
  likeUrl,
  lognamelikesthis,
  post_url,
  clickhandler,
}) {
  const numlikes = num;
  const lognamelikedthis = lognamelikesthis;
  const buttontext = false;
  var like_text = "";
  if (numlikes == 1) {
    like_text = numlikes.toString() + " like";
  } else {
    like_text = numlikes.toString() + " likes";
  }
  return (
    <div className="likeButton">
      <p>{like_text}</p>
      <button onClick={clickhandler} className="like-unlike-button">
        {btext}
      </button>
    </div>
  );
}
