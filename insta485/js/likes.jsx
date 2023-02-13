import React, { useState, useEffect } from 'react';
import PropTypes from "prop-types";
const updateLikes = () => {
    const [numlikes, setNumLikes] = useState(0);
    const [lognamelikedthis, setLognamenameLikedThis] = useState(false);
    const [likeid, setLikeid] = useState(0);
    const [postid, setPostid] = useState(0);
    post_url = url = '/api/v1/posts/'.concat(postid.toString());
    console.log(post_url)
    useEffect(() => {
        fetch(post_url)
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {


                if (!ignoreStaleRequest) {
                    setLognamenameLikedThis(data['likes']['lognameLikesThis'])
                    setNumLikes(data['likes']['numlikes'])
                    setPostid(data['postid'])
                    //setLikeid(data['likes']['url'])
                }
            })
            .catch((error) => console.log(error));
        if (lognameLikesThis) {
            m = "DELETE";
            like_url = "/api/v1/likes/".concat(likeid.toString());
        }
        else { m = "POST"; like_url = "/api/v1/likes/?postid=".concat(postid.toString()); }

        const addLikes = async (lognamelikedthis, numlikes) => {
            let response = await fetch(like_url, {
                method: m
            });
            let data = await response.json();
            setNumLikes(numlikes + 1);
            setLognamenameLikedThis(!lognamelikedthis);

        }
        const deleteLikes = async (lognamelikedthis, numlikes) => {
            let response = await fetch(like_url, {
                method: m
            });
            let data = await response.json();
            setNumLikes(numlikes - 1);
            setLognamenameLikedThis(!lognamelikedthis)

        }

        const handleclick = () => {
            if (lognameLikesThis) {
                deleteLikes(lognamelikedthis, numlikes)
            }
            else {
                addLikes(lognamelikedthis, numlikes)
            }

        }
        //already liked, delete a like 
        return (
            <div className="likes">
                <p>{numlikes} likes</p>
                <button onclick={updateLikes} className="like-unlike-button">
                    like
                </button>
            </div>
        );



    });
};
export default updateLikes;
