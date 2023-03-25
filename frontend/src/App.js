import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import TopBar from './componenets/topbar/topbar';
import Home from './pages/home/home';
import SignIn from './pages/sign-in/sign-in';
import 'bootstrap/dist/css/bootstrap.min.css';
import { AuthProvider } from './contexts/AuthContext';
import SignUp from './pages/sign-up/sign-up';
import ForgotPassword from './pages/forgot-password/forgot-password';

function App() {

  return (
    <Router>
      <div className="App">
        <TopBar/>
        <AuthProvider>
          <Routes>
            <Route path='/' element={<Home/>} />
            <Route path='/sign-in' element={<SignIn/>}/>
            <Route path='/sign-up' element={<SignUp/>}/>
            <Route path='forgot-password' element={<ForgotPassword/>}/>
          </Routes>
        </AuthProvider>
      </div>
    </Router>
  );
}

export default App;
