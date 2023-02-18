import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Comments from "./comments";
import UpdateLikes from "./likes";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
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
  const [likeid, setLikeid] = useState(0);
  const [postShowUrl, setPostShowUrl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  const [likeText, setLikeText] = useState("");
  const [finished, setfinished] = useState(false);
  //var finished = false;
  var like_id;
  var lls = false;
  var like = 0;

  const doSetLikeid = (num) => {
    setLikeid(num);
  };
  useEffect(() => {
    console.log("useEffect");
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
          setlikeurl(data["likes"]["url"]);
          setNumlikes(data["likes"]["numLikes"]);
          setloglikes(data["likes"]["lognameLikesThis"]);
          setTime(moment.utc(data["created"]).fromNow());
          setPostUrl(data["url"]);
          setPostShowUrl(data["postShowUrl"]);
          setOwnerShowUrl(data["ownerShowUrl"]);
          like = data["likes"]["numLikes"];
          // if (like === 1) {
          //   setLikeText("like");
          // } else {
          //   setLikeText("likes")
          // }

          lls = data["likes"]["lognameLikesThis"];
          //get likeid
          like_id = likeurl.replace("/api/v1/likes/", "");
          like_id = like_id.replace("/", "");
          doSetLikeid(Number(like_id));
          if (lls) {
            setButtonText("unlike");
          } else {
            setButtonText("like");
          }
          setfinished(true);
          // if (numLikes == 1) { setLikeText("like"); }
          // else {
          //   setLikeText("likes");
          // }
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

  //   console.log(postUrl);
  //   console.log(postid);
  let like_url;

  const addLikes = (event) => {
    if (loglikes) {
      return;
    }
    like_url = "/api/v1/likes/?postid=".concat(postid.toString());
    fetch("/api/v1/likes/?" + new URLSearchParams({ postid: postid }), {
      credentials: "same-origin",
      method: "POST",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        setlikeurl(data["url"]);
      })
      .catch((error) => console.log(error));
    setNumlikes(numLikes + 1);
    setloglikes(!loglikes);
    setButtonText("unlike");
  };
  const deleteLikes = (event) => {
    like_id = likeurl.replace("/api/v1/likes/", "");
    like_id = like_id.replace("/", "");
    // console.log(Number(like_id));
    // setLikeid(Number(like_id));
    like_url = "/api/v1/likes/" + like_id + "/";
    fetch(like_url, {
      credentials: "same-origin",
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        // return response.json();
      })
      .catch((error) => console.log(error));
    setNumlikes(numLikes - 1);
    setloglikes(!loglikes);
    setButtonText("like");
  };

  const handleclick = () => {
    if (loglikes) {
      deleteLikes();
    } else {
      addLikes();
    }
  };

  function handleDelete(event) {
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
      })
      .catch((error) => console.log(error));

    if (!ignoreStaleRequest) {
      var deleteComment = comments.map((comment) => {
        return comment;
      });
      for (let i = 0; i < deleteComment.length; i++) {
        if (deleteComment[i]["commentid"] == 1.0 * id_to_delete) {
          deleteComment.splice(i, 1);
        }
      }
      setComments([...deleteComment]);
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(event);
    // get a url
    // var postid = postUrl.replace("/api/v1/posts/", "");
    // postid = postid.replace("/", "");
    const searchparams = new URLSearchParams(url);
    var commentUrl = "/api/v1/comments/?postid=" + postid;

    let ignoreStaleRequest = false;
    fetch("/api/v1/comments/?" + new URLSearchParams({ postid: postid }), {
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ text: event.target[0].value }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setComments([...comments, ...[data]]);
          event.target[0].value = "";
        }
      })
      .catch((error) => console.log(error));
  };

  // Render post image and post owner
  if (finished) {
    return (
      <div className="post">
        <a href={ownerShowUrl}>{owner}</a>
        <a href={postShowUrl}>{timeStamp}</a>

        <a href={ownerShowUrl}>
          <img src={ownerImgUrl} alt="owner_image" />
        </a>

        <img src={imgUrl} onDoubleClick={addLikes} alt="post_image" />

        <div className="likeButton">
          <p>
            {numLikes} {numLikes == 1 ? " like" : " likes"}
          </p>

          <button onClick={handleclick} className="like-unlike-button">
            {likeButtonText}
          </button>
        </div>

        <div>
          {comments.map((comment) => {
            // Return HTML for one clue
            if (comment["lognameOwnsThis"]) {
              //setuniqueid(uniqueid + 1)
              return (
                <div key={comment["commentid"]}>
                  <a href={comment["ownerShowUrl"]}> {comment["owner"]}</a>
                  <span className="comment-text">{comment["text"]}</span>
                  <button
                    className="delete-comment-button"
                    onClick={handleDelete}
                    id={comment["commentid"]}
                  >
                    delete
                  </button>
                </div>
              );
            }
            return (
              <div key={comment["commentid"]}>
                <a href={comment["ownerShowUrl"]}> {comment["owner"]}</a>
                <span className="comment-text">{comment["text"]}</span>
              </div>
            );
          })}
          <form className="comment-form" onSubmit={handleSubmit}>
            <input type="text" />
          </form>
        </div>
      </div>
    );
  } else {
    console.log("entered empty");
    return <div></div>;
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
