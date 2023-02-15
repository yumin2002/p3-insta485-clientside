import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Feed({ url }) {
  //  const [pageUrl, setPageUrl] = useState(url);
  // const [postKey, setPostKey] = useState(0)
  var postKey = 0;
  // const [postsUrls, setPostsUrls] = useState(() => {
  const [pageUrl, setPageUrl] = useState("");
  const [postsUrls, setPostsUrls] = useState([]);
  const [hasNext, setHasNext] = useState(false);
  const [fetchNext, setFetchNext] = useState(true);

  useEffect(() => {
    console.log(pageUrl);
    console.log(postsUrls);
    console.log(hasNext);
    console.log(fetchNext);
    var initialPosts = [];
    if (!fetchNext) {
      return;
    }
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
          //   setPageUrl("");
          setPostsUrls([...initialPosts]);
        } else {
          setHasNext(true);
          setPageUrl(data["next"]);
          setPostsUrls([...initialPosts]);
        }
      })
      .catch((error) => console.log(error));
  }, [fetchNext, pageUrl, postsUrls]);

  // Render post image and post owner
  return (
    <InfiniteScroll
      dataLength={postsUrls.length} //This is important field to render the next data
      next={() => {
        setFetchNext(true);
      }}
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
        postKey = postKey + 1;
        return <Post url={postUrl} key={postKey} />;
      })}
    </InfiniteScroll>
  );
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};
