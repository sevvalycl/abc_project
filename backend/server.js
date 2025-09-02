const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const abcRoute = require('./routes/abc');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Python çıktısı ve dosyaları için statik klasör
app.use('/files', express.static(path.join(__dirname, 'python/files')));

// Frontend dosyaları için statik klasör
app.use('/', express.static(path.join(__dirname, '../frontend')));

app.use('/api/abc', abcRoute);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Sunucu ${PORT} portunda çalışıyor`);
    console.log(`http://localhost:${PORT}`);
});
