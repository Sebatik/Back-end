const response = require('../middleware/response')
const connection = require('../config/connection');
const verifyToken = require('../middleware/verifyToken')

// Get All Batik
const getAllBatik = (req, res) => {
    // Verify Token
    const authHeader = req.headers.authorization;
        
    if(!authHeader || !authHeader.startsWith('Bearer ')) {
        return response(403,null,"Unauthorized",res)
    }

    // Ambil token dari header
    const token = authHeader.split(' ')[1];

    // Verifikasi token menggunakan fungsi verifyToken
    verifyToken(token)
        .then(decodedToken => {
            // Dapatkan informasi pengguna dari payload token
            console.log(decodedToken);

            // Lakukan apa pun yang perlu Anda lakukan dengan informasi pengguna ini, misalnya memperbarui query atau memberikan akses sesuai dengan informasi pengguna.
            
            const query = 'SELECT * FROM batik';
            connection.query(query, (err, results) => {
                if (err) {
                    console.error('Error fetching data:', err);
                    return response(500,null,"Error Fetching Data",res)
                }
                response(200,results,"Batiks Retrieved",res)
            });
        })
        .catch(err => {
            console.error('Error verifying token:', err);
            return response(403,err,"Unauthorized",res);
        });
};

const getAllBatikPosts = async (req,res) => {
    res.send('Get All Batik Post')
}

module.exports = {
    getAllBatik,
    getAllBatikPosts
}