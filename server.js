// create express app
const express = require('express');
// handling file uploads
const multer = require('multer');
// handle tasks without waiting
const { spawn } = require('child_process');
const sql = require('mssql');
const path = require('path');
// file system
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Set up multer for handling file uploads
const upload = multer({ dest: 'uploads/' }); // Define the directory to store uploaded files

app.use('/images', express.static(path.join(__dirname, 'images')));


// Parse incoming requests with JSON payloads
app.use(bodyParser.json());
// Parse incoming requests with urlencoded payloads
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));


// Your config object
const config = {
// add your database config here
};


// Endpoint to fetch data from database
app.get('/fetchData', async (req, res) => {
  try {
    // Connect to database
    await sql.connect(config);
    
    // Query to fetch data from DetectedObjects table
    const result = await sql.query`SELECT * FROM DetectedObjects`;
    
    // Send the data as response
    res.json(result.recordset);
  } catch (error) {
    console.error('Error fetching data from database:', error);
    res.status(500).send('Error fetching data from database');
  } finally {
    // Close the database connection
    await sql.close();
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});