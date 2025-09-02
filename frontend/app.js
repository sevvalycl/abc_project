const funcSelect = document.getElementById('funcSelect');
const customFunc = document.getElementById('customFunc');
const runBtn = document.getElementById('runBtn');
const resultPre = document.getElementById('result');
const graphImg = document.getElementById('graph');
const downloadCsv = document.getElementById('downloadCsv');
const downloadGraph = document.getElementById('downloadGraph');

// fonksiyon seçiminde custom kutusu aç kapat
funcSelect.addEventListener('change', () => {
    customFunc.style.display = (funcSelect.value === 'custom') ? 'inline-block' : 'none';
});

// çalıştır butonu
runBtn.addEventListener('click', async () => {
    const payload = {
        funcName: funcSelect.value,
        dim: parseInt(document.getElementById('dim').value),
        maxIter: parseInt(document.getElementById('maxIter').value),
        foodNumber: parseInt(document.getElementById('foodNumber').value),
        limit: parseInt(document.getElementById('limit').value),
        customExpr: customFunc.value
    };

    // çalıştırmadan önce tüm görselleri ve linkleri gizle
    graphImg.style.display = 'none';
    downloadGraph.style.display = 'none';
    downloadCsv.style.display = 'none';
    resultPre.textContent = 'Çalışıyor...';

    try {
        const res = await fetch('http://localhost:5000/api/abc', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.error) {
            resultPre.textContent = "Hata: " + data.error;
        } else {
            resultPre.textContent = `En iyi çözüm: ${data.best_sol}\nEn iyi fitness: ${data.best_fit}`;

            // grafik göster ve indirilebilir yap
            graphImg.src = data.graph_file || '/files/abc_graph.png';
            graphImg.style.display = 'block';
            downloadGraph.href = data.graph_file || '/files/abc_graph.png';
            downloadGraph.style.display = 'inline-block';

            // CSV indirme linki
            downloadCsv.href = data.csv_file || '/files/abc_results.csv';
            downloadCsv.style.display = 'inline-block';
        }
    } catch (err) {
        resultPre.textContent = "Sunucuya bağlanırken hata: " + err;
    }
});
