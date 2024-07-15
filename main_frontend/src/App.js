import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import './style.css';
// import './font-awesome.min.css';
// import './bootstrap.min.css';
import Details from './Components/Details';
import Posts from './Components/Posts';
import Nav from './Components/Nav';
import Login from './Components/Login';
import Signuppage from './Components/Signup';
import Channelshow from './Components/Channelshow';
import Chat from './Components/Chat';
import Home from './Components/Home';

const App = () => {
    return (
        <Router>
            <Nav/>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/forum" element={<Posts/>}/>
                <Route path="/channel/:channelName" element={<Chat/>}/>
                <Route path="/top-comments" element={<Details/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/signup" element={<Signuppage/>}/>
                <Route path="/my-channels" element={<Channelshow/>}/>
                
                
            </Routes>
        </Router>
    );
};

export default App;
