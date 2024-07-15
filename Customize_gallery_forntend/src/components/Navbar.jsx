// // src/components/Navbar.js
// import React from 'react';
// import { Link } from 'react-router-dom';

// const Navbar = () => {
//     return (
//         <nav>
//             <ul>
                
//                 <li>
//                     <Link to="/gallery">Gallery</Link>
//                 </li>
//             </ul>
//         </nav>
//     );
// };

// export default Navbar;


import './Navbar.css';

import { Link, useLocation, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const handleLogout = () => {
        localStorage.removeItem('email');
        navigate('/login');
    }
    return (
        <div className="nav">
            <Link to="/" className=' px-[4rem] font-bold text-3xl my-auto'>Myntra</Link>

            <ul className='pl-8 flex justify-between w-[35%] my-auto'>
                <Link to='/forum' className='flex cursor-pointer'>Forum</Link>
                <Link to='/top-comments' className='flex cursor-pointer'>Top Comments</Link>
                <Link to='/my-channels' className='flex cursor-pointer'>My Channel</Link>
                
            </ul>

            <div className="ml-auto my-auto pr-[6rem]">
                {!localStorage.getItem('email') ? (<>
                    <Link className={`link ${location.pathname === '/login' ? "active" : ""}`} to='/login'>Login</Link>
                    <Link className={`link ${location.pathname === '/signup' ? "active" : ""}`} to='/signup'>Signup</Link>
                </>)
                    :
                    (<h5 className="nav_logout" onClick={handleLogout}>Logout</h5>)}
            </div>

        </div>
    )
}

export default Navbar;