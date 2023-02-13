import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Comments from "./comments";
import UpdateLikes from "./likes";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */
  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [ownerImgUrl, setOwnerImg] = useState("");
  const [timeStamp, setTime] = useState("");
  const [numLikes, setNumlikes] = useState(0);
  const [loglikes, setloglikes] = useState(false);
  const [likeurl, setlikeurl] = useState("");
  const [comments, setComments] = useState([]);
  const [postUrl, setPostUrl] = useState("");
  const [likeButtonText, setButtonText] = useState("button");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          const commentLists = [];
          for (var i = 0, size = data["comments"].length; i < size; i++) {
            commentLists.push(data["comments"][i]["text"]);
          }
          setComments(data["comments"]);
          //   print(data["comments"]);
          setImgUrl(data["imgUrl"]);
          setOwner(data["owner"]);
          setOwnerImg(data["ownerImgUrl"]);
          setlikeurl(data["likes"]["url"])
          setNumlikes(data["likes"]["numLikes"])
          setloglikes(data["likes"]["lognameLikesThis"])
          setTime(moment.utc(data["created"]).fromNow());
          setPostUrl(data["url"]);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  var postid = postUrl.replace("/api/v1/posts/", "");
  postid = postid.replace("/", "");
  //post_url = "/api/v1/comments/?postid=" + postid;
  //if not liked, like url will be null

  var likeid;


  console.log(postUrl);
  console.log(postid);
  let m;
  let like_url;
  if (loglikes) {
    m = "DELETE";
    likeid = likeurl.replace("/api/v1/likes/", "");
    likeid = likeid.replace("/", "");
    like_url = "/api/v1/likes/".concat(likeid.toString()) + "/";
  }
  else { m = "POST"; like_url = "/api/v1/likes/?postid=".concat(postid.toString()); }
  console.log(like_url)

  const addLikes = (event) => {
    let ignoreStaleRequest = false;
    fetch(like_url,
      { credentials: "same-origin", method: m })
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
    setNumlikes(numLikes + 1);
    setloglikes(!loglikes);
    setButtonText("unlike");

  }
  const deleteLikes = (event) => {
    let ignoreStaleRequest = false;
    fetch(like_url,
      {
        credentials: "same-origin", method: m, headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        // return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
        }
      })
      .catch((error) => console.log(error));
    setNumlikes(numLikes - 1);
    setloglikes(!loglikes);
    setButtonText("like");
  }

  const handleclick = () => {
    if (loglikes) {
      deleteLikes()
    }
    else {
      addLikes()
    }

  };

  // Render post image and post owner
  return (
    <div className="post">
      <p>{owner}</p>
      <p>{timeStamp}</p>
      <img src={ownerImgUrl} alt="owner_image" />
      <img src={imgUrl} alt="post_image" />
      <UpdateLikes btext={likeButtonText} num={numLikes} likeUrl={likeurl} lognamelikesthis={loglikes} post_url={postUrl} clickhandler={handleclick} />
      <Comments url={postUrl} comments={comments} />
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
