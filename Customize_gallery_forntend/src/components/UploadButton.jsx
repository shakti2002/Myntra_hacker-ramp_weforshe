
// import React, { useState } from 'react';
// import axios from 'axios';

// const UploadButton = () => {
//     const [selectedFile, setSelectedFile] = useState(null);
//     const [preview, setPreview] = useState(null);
//     const [recommendations, setRecommendations] = useState([]);

//     const handleFileChange = (event) => {
//         const file = event.target.files[0];
//         setSelectedFile(file);
//         setPreview(URL.createObjectURL(file));
//     };

//     const handleUpload = async () => {
//         if (!selectedFile) return;
//         const formData = new FormData();
//         formData.append('image', selectedFile);
//         try {
//             const response = await axios.post('http://localhost:80/upload', formData, {
//                 headers: {
//                     'Content-Type': 'multipart/form-data'
//                 }
//             });
//             alert('Image uploaded successfully');
//             setRecommendations(response.data.recommendations);
//         } catch (error) {
//             console.error('Error uploading image:', error);
//             alert('Error uploading image');
//         }
//     };

//     return (
//         <div>
//             <input type="file" onChange={handleFileChange} />
//             {preview && <img src={preview} alt="Preview" style={{ width: '100px', height: '100px' }} />}
//             <button onClick={handleUpload}>Upload Image</button>
//             <div>
//                 {recommendations.length > 0 && (
//                     <div>
//                         <h3>Recommended Images:</h3>
//                         <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '10px' }}>
//                             {recommendations.map((rec, index) => (
//                                 <img key={index} src={`http://localhost:80/imagefile/${rec}`} alt={`Recommendation ${index}`} style={{ width: '100px', height: '100px' }} />
//                             ))}
//                         </div>
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// };

// export default UploadButton;

import React, { useState } from 'react';
import axios from 'axios';
import './UploadButton.css';

const UploadButton = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [recommendations, setRecommendations] = useState([]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setPreview(URL.createObjectURL(file));
    };

    const handleUpload = async () => {
        if (!selectedFile) return;
        const formData = new FormData();
        formData.append('image', selectedFile);
        try {
            const response = await axios.post('http://localhost:80/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert('Image uploaded successfully');
            setRecommendations(response.data.recommendations);
        } catch (error) {
            console.error('Error uploading image:', error);
            alert('Error uploading image');
        }
    };

    return (
        <div className="upload-container">
            <h1>Upload Your custom design</h1>
            <input type="file" onChange={handleFileChange} />
            {preview && <img src={preview} alt="Preview" className="preview-image" />}
            <button className="upload-button" onClick={handleUpload}>Upload Image</button>
            <div>
                {recommendations.length > 0 && (
                    <div>
                        <h1>Recommended Images:</h1>
                        <div className="recommendation-grid">
                            {recommendations.map((rec, index) => (
                                <div className="image-card" key={index}>
                                    <img src={`http://localhost:80/imagefile/${rec}`} alt={`Recommendation ${index}`} className="image" />
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadButton;


