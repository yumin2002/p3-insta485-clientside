import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import moment from 'moment';

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  console.log(url)
  console.log("debug")

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [ownerImgUrl, setOwnerImg] = useState("");
  const [timeStamp, setTime] = useState("");
  const [numLikes, setNumlikes] = useState("");
  const [comments, setComments] = useState("");
  const [likeButton, setlikeButton] = useState("");
  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    //using 2 fetches to construct a list of post info

    // Call REST API to get the post's information
    async function fetchData() {
      const response = await fetch(url, { credentials: "same-origin" })
      if (!ignoreStaleRequest) {
        const data = await response.json();
        const commentLists = []
        for (var i = 0, size = data['comments'].length; i < size; i++) {
          commentLists.push(data['comments'][i]['text'])
        }
        setComments([...commentLists])
        setImgUrl(data['imgUrl'])
        setOwner(data['owner'])
        setOwnerImg(data['ownerImgUrl'])
        setNumlikes(data['likes']['numLikes'])
        setTime(moment.utc(data['created']))
        if (data['likes']['lognameLikesThis']) {
          setlikeButton("unlike")
        } else {
          setlikeButton('like')
        }
        var day = moment("")
        console.log(moment.utc(data['created']))
        console.log(moment.utc(data['created']).fromNow())
      }

    }
    fetchData()






    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  // Render post image and post owner

  return (
    <div className="post">
      <img src={imgUrl} alt="post_image" />
      <p>{owner}</p>
      <p>{timeStamp}</p>
      <p>{numLikes}</p>
      <img src={ownerImgUrl} alt="owner_image" />
      <p>{comments}</p>
      <button type='"button'>{likeButton}</button>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
