require('dotenv').config(); // Load environment variables
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const connection = require('./src/config/connection');

const app = express();
const port = 8080;

// Initialize server
app.use(express.urlencoded({ extended: true }));
app.use(cors());
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send('Sebatik API')
  })

// API Sebatik
app.use('/batik', require('./src/routes/batikRoutes'));

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
