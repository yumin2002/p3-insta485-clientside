import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Feed({ url }) {
  const [postsUrls, setPostsUrls] = useState([
    "/api/v1/posts/1/",
    "/api/v1/posts/1/",
    "/api/v1/posts/1/",
    "/api/v1/posts/1/",
    "/api/v1/posts/1/",
    "/api/v1/posts/1/",
    "/api/v1/posts/1/",
  ]);
  //   useEffect(() => {
  //     setPostsUrls([
  //       "/api/v1/posts/1/",
  //       "/api/v1/posts/1/",
  //       "/api/v1/posts/1/",
  //       "/api/v1/posts/1/",
  //       "/api/v1/posts/1/",
  //       "/api/v1/posts/1/",
  //       "/api/v1/posts/1/",
  //     ]);
  //   });
  function fetchData() {
    setPostsUrls([...postsUrls, ["/api/v1/posts/1/"]]);
    console.log(postsUrls);
  }

  // Render post image and post owner
  return (
    <InfiniteScroll
      dataLength={postsUrls} //This is important field to render the next data
      next={fetchData}
      hasMore={true}
      loader={<h4>Loading...</h4>}
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
