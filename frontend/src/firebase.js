// Import the functions you need from the SDKs you need
import firebase from "firebase/compat/app";
import "firebase/compat/auth"
import "firebase/compat/storage"
import { getFirestore } from 'firebase/firestore';

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const app = firebase.initializeApp({
  apiKey: "AIzaSyBknp-PEUNLaPqv7-Sr6HameMNFRXZi6WU",
  authDomain: "usuhack-6795c.firebaseapp.com",
  projectId: "usuhack-6795c",
  storageBucket: "usuhack-6795c.appspot.com",
  messagingSenderId: "975453514366",
  appId: "1:975453514366:web:2777ca36439b10ed03c62f",
  measurementId: "G-11MZME22ZJ"
})

export const db = getFirestore(app)
export const storage = firebase.storage()
export const auth = app.auth()
export default app