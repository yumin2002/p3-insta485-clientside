import React, { useState, useEffect } from 'react';
import PropTypes from "prop-types";
export default function UpdateLikes({ likes }) {
    const [numlikes, setNumLikes] = useState(0);
    const [lognamelikedthis, setLognamenameLikedThis] = useState(false);
    const [buttontext, setButtonText] = useState('like');
    // const [likeid, setLikeid] = useState(0);
    // const [postid, setPostid] = useState(0);
    post_url = '/api/v1/posts/'.concat(postid.toString());
    console.log(post_url)

    if (likes['lognameLikesThis']) {
        m = "DELETE";
        like_url = "/api/v1/likes/".concat(likeid.toString());
    }
    else { m = "POST"; like_url = "/api/v1/likes/?postid=".concat(postid.toString()); }

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
        setNumLikes(numlikes + 1);
        setLognamenameLikedThis(!lognamelikedthis);
        setButtonText("unlike");

    }
    const deleteLikes = (event) => {
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
        setNumLikes(numlikes - 1);
        setLognamenameLikedThis(!lognamelikedthis);
        setButtonText("like");

    }

    const handleclick = () => {
        if (lognameLikesThis) {
            deleteLikes(lognamelikedthis, numlikes)
        }
        else {
            addLikes(lognamelikedthis, numlikes)
        }

    };
    return (
        <div className="likeButton">
            <p>{numlikes} likes</p>
            <button onclick={handleclick} className="like-unlike-button">
                {buttontext}
            </button>
        </div>
    );
}
