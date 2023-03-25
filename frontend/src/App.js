import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import TopBar from './componenets/topbar/topbar';
import Home from './pages/home/home';
import SignIn from './pages/sign-in/sign-in';
import 'bootstrap/dist/css/bootstrap.min.css';
import { AuthProvider } from './contexts/AuthContext';
import SignUp from './pages/sign-up/sign-up';
import ForgotPassword from './pages/forgot-password/forgot-password';
import User from './pages/user/user';
import AllPlayers from './pages/all-players/all-players';

function App() {

  return (
    <Router>
      <div className="App">
        <AuthProvider>
        <TopBar/>
          <Routes>
            <Route path='/' element={<Home/>} />
            <Route path='/all-players' element={<AllPlayers/>}/>
            <Route path='/forgot-password' element={<ForgotPassword/>}/>
            <Route path='/sign-in' element={<SignIn/>}/>
            <Route path='/sign-up' element={<SignUp/>}/>
            <Route path='/user' element={<User/>}/>
          </Routes>
        </AuthProvider>
      </div>
    </Router>
  );
}

export default App;
