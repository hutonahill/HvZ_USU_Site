import React, { useContext, useState, useEffect } from 'react'
import { auth } from '../firebase'
import { useNavigate } from 'react-router-dom'

const AuthContext = React.createContext()

export function useAuth() {
   return useContext(AuthContext)
}
//Firebase auth functions that provide navigation depending on function 
export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState()
    const [loading, setLoading] = useState(true)
    const [mongoUser, setMongoUser] = useState()
    

    const navigate = useNavigate();

    function signup(email, password) {
        return auth.createUserWithEmailAndPassword(email, password)
    }

    function login(email, password) {
        return auth.signInWithEmailAndPassword(email, password)
    }

    // uses signOut function from firebase/auth next we append .then to navigate the user back to the homepage

   function logout() {
        return auth.signOut().then(() =>
        navigate('/')
        )
    }

    function resetPassword(email) {
        return auth.sendPasswordResetEmail(email)
    }

    /*
        This useEffect is for the initial render of this component, sets up a event listener for the state.
    */
    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged( user => {
            setCurrentUser(user)
            setLoading(false)
        })
        return unsubscribe
    })

    const value = {
        currentUser,
        login,
        signup,
        logout,
        resetPassword
    }

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    )
}
