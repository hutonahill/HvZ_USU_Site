import axios from "axios";
import { useState } from "react";

export function getUser() {
    let result = '';
    axios.get('localhost:5000/').then((res) => JSON.parse(res)).then((res) => result = res).catch((err) => console.log(err))
    return result;
}