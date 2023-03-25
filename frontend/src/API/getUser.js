import axios from "axios";
import { useState } from "react";

export async function getUser(uid) {
    let result = [];
    fetch(`http://localhost:5000/getSingleUserData/${uid}`, {
        method: "GET", // or 'PUT'
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
        //   "Content-Type": "",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
  .then((response) => {response.json()})
  .then((data) => 
        {result = data.userData})
    .catch(err => console.log(err));

    return result;
}