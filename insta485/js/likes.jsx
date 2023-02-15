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
  // const [numlikes, setNumLikes] = useState(num);
  // const [lognamelikedthis, setLognamenameLikedThis] = useState(false);
  // const [buttontext, setButtonText] = useState('like');
  // const [likeid, setLikeid] = useState(0);
  // const [postid, setPostid] = useState(0);

  const numlikes = num;
  const lognamelikedthis = lognamelikesthis;
  const buttontext = false;
  var like_text = "";
  //if logname doesnot like this, likeurl is null
  // var postid = post_url.replace("/api/v1/posts/", "");
  // postid = postid.replace("/", "");
  // //post_url = "/api/v1/comments/?postid=" + postid;
  // //if not liked, like url will be null

  // var likeid;
  // // if (likeUrl != "") {

  // // }

  // console.log(post_url);
  // console.log(postid);
  // // useEffect(() => {
  // let m;
  // let like_url;
  // if (lognamelikesthis) {
  //     m = "DELETE";
  //     likeid = likeUrl.replace("/api/v1/likes/", "");
  //     likeid = likeid.replace("/", "");
  //     like_url = "/api/v1/likes/".concat(likeid.toString()) + "/";
  // }
  // else { m = "POST"; like_url = "/api/v1/likes/?postid=".concat(postid.toString()); }
  // console.log(like_url)

  //}, [numlikes, lognamelikedthis]);
  if (numlikes == 1) { like_text = numlikes.toString() + " like" }
  else {
    like_text = numlikes.toString() + " likes"
  }
  return (
    <div className="likeButton">


      <p>{like_text}</p>
      <button onClick={clickhandler} class="like-unlike-button">
        {btext}
      </button>
    </div>
  );
}
