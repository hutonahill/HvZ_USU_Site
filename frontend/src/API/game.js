import axios from "axios";

export function getGameState() {
    let result = '';
    axios.get('localhost:5000/game-state').then((res) => JSON.parse(res)).then((res) => result = res).catch((err) => console.log(err));
    return result;
}