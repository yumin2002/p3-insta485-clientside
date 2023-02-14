import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Feed({ url }) {
  const [pageUrl, setPageUrl] = useState(url);
  const [postsUrls, setPostsUrls] = useState(() => {
    var initialPosts = [];
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        initialPosts = data["results"].map((result) => {
          return result["url"];
        });
        if (data["next"] == "") {
          setHasNext(false);
          setPageUrl("");
        } else {
          setHasNext(true);
          setPageUrl(data["next"]);
        }
      })
      .catch((error) => console.log(error));
    return [...initialPosts];
  });
  const [hasNext, setHasNext] = useState(true);

  function fetchData(curr_pageUrl) {
    console.log(hasNext);
    console.log(curr_pageUrl);
    console.log(pageUrl);
    console.log(postsUrls);
    var newPosts = [];
    fetch(curr_pageUrl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        newPosts = data["results"].map((result) => {
          return result["url"];
        });
        if (data["next"] == "") {
          setHasNext(false);
          setPageUrl("");
          setPostsUrls([...postsUrls, ...newPosts]);
        } else {
          setPageUrl(data["next"]);
          setPostsUrls([...postsUrls, ...newPosts]);
        }
      })
      .catch((error) => console.log(error));
  }

  // Render post image and post owner
  return (
    <InfiniteScroll
      dataLength={postsUrls} //This is important field to render the next data
      next={fetchData(pageUrl)}
      hasMore={hasNext}
      loader={<h4>Loading...</h4>}
      scrollThreshold="200px"
      endMessage={
        <p style={{ textAlign: "center" }}>
          <b>Yay! You have seen it all</b>
        </p>
      }
    >
      {postsUrls.map((postUrl) => {
        return <Post url={postUrl} />;
      })}
    </InfiniteScroll>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
