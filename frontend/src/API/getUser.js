import axios from "axios";
import { useState } from "react";

export function getUser(uid) {
    let result = [];
    axios.get(`http://localhost:5000/getSingleUserData/${uid}`).then((res) => JSON.parse(res)).then((res) => result = res).catch((err) => console.log(err))
    fetch(`http://localhost:5000/getSingleUserData/${uid}`)
  .then((response) => response.json())
  .then((data) => 
        {console.log(data)
        result = data.userData[1]});

    return result;
}