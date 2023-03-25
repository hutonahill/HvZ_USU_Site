import axios from "axios";
import { useState } from "react";

export function getUser(uid) {
    let result = [];
    axios.get(`http://localhost:5000/getSingleUserData/${uid}`).then((res) => JSON.parse(res)).then((res) => result = res).catch((err) => console.log(err))
    return result;
}