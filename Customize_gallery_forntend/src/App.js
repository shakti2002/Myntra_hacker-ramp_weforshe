// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import UploadButton from './components/UploadButton';
import GalleryPage from './components/GalleryPage';

function App() {
    return (
        <Router>
            <div className="App">
                {/* <Navbar /> */}
                {/* <UploadButton/> */}
                {/* <GalleryPage/> */}
                <Routes>/
                    {/* <Route path="/" exact component={UploadButton} /> */}
                    <Route path='/gallery'  element={< GalleryPage/>}/>
                    <Route path='/custom'  element={< UploadButton/>}/>
                    
                </Routes>
            </div>
        </Router>
    );
}

export default App;
