import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Feed({ url }) {
  console.log(getPosts(url));
  const [postsUrls, setPostsUrls] = useState(getPosts(url));
  const [hasMore, setHasMore] = useState(true);

  function getPosts(curr_url) {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    var initialPosts = [];
    // Call REST API to get the post's information
    fetch(curr_url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        initialPosts = data["results"].map((curr) => {
          return curr["url"];
        });
      })
      .catch((error) => console.log(error));
    console.log(initialPosts);
    return initialPosts;
  }

  function getMorePost() {
    var curr_url = url;
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    // Call REST API to get the post's information
    fetch(curr_url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          console.log(data["next"]);
          console.log(date["result"]);
          if (data["next"] == "") {
            setHasMore(false);
          } else {
            setHasMore(true);
          }
          setPostsUrls(
            data["results"].map((curr) => {
              return curr["url"];
            })
          );
          console.log(hasMore);
          console.log(postsUrls);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }

  // Render post image and post owner
  return (
    <InfiniteScroll
      dataLength={postsUrls.length}
      next={getMorePost}
      hasMore={hasMore}
      loader={<h3> Loading...</h3>}
      endMessage={<h4>Nothing more to show</h4>}
    >
      <div>
        {postsUrls.map((postUrl) => {
          return (
            <div>
              <Post url={postUrl} />
            </div>
          );
        })}
      </div>
    </InfiniteScroll>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
