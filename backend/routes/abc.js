const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

router.post('/', (req, res) => {
    const { funcName, dim, maxIter, foodNumber, limit, customExpr } = req.body;

    const args = [
        funcName,
        dim,
        maxIter,
        foodNumber,
        limit
    ];
    if (funcName === 'custom') args.push(customExpr);

    const pyPath = path.join(__dirname, '../python/abc.py');
    const py = spawn('python', [pyPath, ...args]);

    let data = '';
    let errData = '';

    py.stdout.on('data', chunk => data += chunk.toString());
    py.stderr.on('data', chunk => errData += chunk.toString());

    py.on('close', code => {
        if (errData) {
            console.error('Python Hatası:\n', errData); // terminalde görünür
            res.status(500).json({ error: errData });
        } else {
            try {
                const result = JSON.parse(data);
                console.log('Python çıktısı:', result); // terminalde JSON görünür

                // Grafik ve CSV dosyalarının frontend tarafından erişilebilir yolu
                result.graph_file = `/files/${result.graph_file}`;
                result.csv_file = `/files/${result.csv_file}`;

                res.json(result);
            } catch (e) {
                console.error('JSON Parse Hatası:', e, '\nPython’dan gelen:', data);
                res.status(500).json({ error: 'Python’dan geçersiz JSON geldi.' });
            }
        }
    });
});

module.exports = router;
