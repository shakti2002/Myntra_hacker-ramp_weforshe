// // src/components/GalleryPage.js
// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// const GalleryPage = () => {
//     const [images, setImages] = useState([]);
//     const [sortByRating, setSortByRating] = useState(false);

//     useEffect(() => {
//         fetchImages();
//     }, [sortByRating]);

//     const fetchImages = async () => {
//         try {
//             const response = await axios.get('http://localhost:80/images', {
//                 params: { sort_by_rating: sortByRating },
//             });
//             setImages(response.data);
//         } catch (error) {
//             console.error('Error fetching images:', error);
//         }
//     };

//     return (
//         <div>
//             <button onClick={() => setSortByRating(!sortByRating)}>
//                 {sortByRating ? 'Unsort by Rating' : 'Sort by Rating'}
//             </button>
//             <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
//                 {images.map((image) => (
//                     <div key={image.filename}>
//                         <img src={`http://localhost:80/uploads/${image.filename}`} alt={image.filename} style={{ width: '100%' }} />
//                         <div>Rating: {image.rating.toFixed(2)}</div>
//                         <div>Comments: {image.comments.length}</div>
//                     </div>
//                 ))}
//             </div>
//         </div>
//     );
// };

// export default GalleryPage;




// src/components/GalleryPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GalleryPage.css';

const GalleryPage = () => {
    const [images, setImages] = useState([]);
    const [sortByRating, setSortByRating] = useState(false);

    useEffect(() => {
        fetchImages();
    }, [sortByRating]);

    const fetchImages = async () => {
        try {
            const response = await axios.get('http://localhost:80/images', {
                params: { sort_by_rating: sortByRating },
            });
            setImages(response.data);
        } catch (error) {
            console.error('Error fetching images:', error);
        }
    };

    return (
        <div className="gallery-container">
            <h1>Your Custom Gallery</h1>
            <button className="sort-button" onClick={() => setSortByRating(!sortByRating)}>
                {sortByRating ? 'Unsort by Rating' : 'Sort by Rating'}
            </button>
            <div className="image-grid">
                {images.map((image) => (
                    <div className="image-card" key={image.filename}>
                        <img src={`http://localhost:80/uploads/${image.filename}`} alt={image.filename} className="image" />
                        <div className="image-info">
                            <div className="rating">⭐ {image.rating.toFixed(2)}</div>
                            <div className="comments">
                                <span className="comment-icon">💬</span> {image.comments.length}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GalleryPage;
