# web_app.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import hashlib
import json
from qr_core import generate_qr_image, save_qr_image, scan_qr_from_file

app = FastAPI(title="QR Code Tool Web", description="Генерация и сканирование QR-кодов онлайн")

# Добавляем CORS для локальной разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём временную папку для файлов
TEMP_DIR = tempfile.mkdtemp()
print(f"📁 Временная папка: {TEMP_DIR}")

# HTML интерфейс
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Tool - Генерация и сканирование</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .tab-btn {
            flex: 1;
            padding: 12px;
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            font-size: 16px;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.3s;
        }

        .tab-btn.active {
            background: white;
            color: #667eea;
        }

        .tab-btn:hover {
            background: rgba(255,255,255,0.3);
        }

        .tab-content {
            display: none;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.5s;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        textarea, input[type="text"], input[type="file"], input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        textarea:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }

        textarea {
            resize: vertical;
            font-family: monospace;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn:active {
            transform: translateY(0);
        }

        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        }

        .result img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }

        .result-text {
            margin-top: 15px;
            padding: 10px;
            background: white;
            border-radius: 8px;
            word-break: break-all;
        }

        .copy-btn {
            margin-top: 10px;
            background: #28a745;
        }

        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }

        .loading.active {
            display: block;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            color: #dc3545;
            margin-top: 10px;
        }

        @media (max-width: 600px) {
            .container {
                padding: 10px;
            }
            .tab-content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ QR Code Tool</h1>
            <p>Генерация и сканирование QR-кодов онлайн</p>
        </div>

        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('generate')">📝 Создать QR</button>
            <button class="tab-btn" onclick="switchTab('scan')">📷 Сканировать QR</button>
        </div>

        <div id="generate-tab" class="tab-content active">
            <form id="generate-form">
                <div class="form-group">
                    <label>📝 Текст или URL:</label>
                    <textarea id="text-input" rows="4" placeholder="Введите текст или URL..."></textarea>
                </div>
                <div class="form-group">
                    <label>🔲 Размер (пиксели):</label>
                    <input type="number" id="size-input" value="250" min="100" max="500" step="10">
                </div>
                <button type="submit" class="btn">Создать QR код</button>
            </form>
            <div id="generate-result" class="result" style="display:none;"></div>
        </div>

        <div id="scan-tab" class="tab-content">
            <form id="scan-form">
                <div class="form-group">
                    <label>📷 Выберите изображение:</label>
                    <input type="file" id="file-input" accept="image/*" required>
                </div>
                <button type="submit" class="btn">Сканировать QR код</button>
            </form>
            <div id="scan-result" class="result" style="display:none;"></div>
        </div>

        <div id="loading" class="loading">
            <div class="spinner"></div>
            <p>Обработка...</p>
        </div>
    </div>

    <script>
        function switchTab(tab) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

            if (tab === 'generate') {
                document.getElementById('generate-tab').classList.add('active');
                document.querySelector('.tab-btn:first-child').classList.add('active');
            } else {
                document.getElementById('scan-tab').classList.add('active');
                document.querySelector('.tab-btn:last-child').classList.add('active');
            }
        }

        document.getElementById('generate-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('text-input').value;
            const size = document.getElementById('size-input').value;

            if (!text) {
                alert('Введите текст для QR кода');
                return;
            }

            showLoading(true);

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text, size: parseInt(size)})
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Ошибка генерации');
                }

                const data = await response.json();

                const resultDiv = document.getElementById('generate-result');
                resultDiv.innerHTML = `
                    <img src="${data.image_path}" alt="QR Code">
                    <div class="result-text">
                        <strong>Содержимое:</strong><br>
                        ${escapeHtml(data.text)}
                    </div>
                    <button class="btn copy-btn" onclick="copyText('${escapeHtml(data.text)}')">📋 Копировать текст</button>
                `;
                resultDiv.style.display = 'block';
            } catch (error) {
                alert('Ошибка: ' + error.message);
            } finally {
                showLoading(false);
            }
        });

        document.getElementById('scan-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const file = document.getElementById('file-input').files[0];

            if (!file) {
                alert('Выберите файл');
                return;
            }

            showLoading(true);

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/scan', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Ошибка сканирования');
                }

                const data = await response.json();

                const resultDiv = document.getElementById('scan-result');
                resultDiv.innerHTML = `
                    <img src="${data.image_path}" alt="Scanned Image" style="max-width: 300px;">
                    <div class="result-text">
                        <strong>📄 Результат сканирования:</strong><br>
                        ${escapeHtml(data.result)}
                    </div>
                    <button class="btn copy-btn" onclick="copyText('${escapeHtml(data.result)}')">📋 Копировать результат</button>
                `;
                resultDiv.style.display = 'block';
            } catch (error) {
                alert('Ошибка: ' + error.message);
            } finally {
                showLoading(false);
            }
        });

        function showLoading(show) {
            document.getElementById('loading').classList.toggle('active', show);
        }

        function copyText(text) {
            navigator.clipboard.writeText(text);
            alert('Текст скопирован в буфер обмена!');
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE


@app.post("/generate")
async def generate_qr(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        text = data.get('text')
        size = data.get('size', 250)

        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        img = generate_qr_image(text, size)
        hash_name = hashlib.md5(f"{text}_{size}".encode()).hexdigest()
        file_name = f"qr_{hash_name}.png"
        file_path = os.path.join(TEMP_DIR, file_name)
        save_qr_image(img, file_path)

        return {"image_path": f"/temp/{file_name}", "text": text}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/scan")
async def scan_qr(file: UploadFile = File(...)):
    try:
        # Сохраняем загруженный файл
        file_path = os.path.join(TEMP_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Сканируем
        result = scan_qr_from_file(file_path)
        return {"result": result, "image_path": f"/temp/{file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/temp/{file_name}")
async def get_temp_file(file_name: str):
    full_path = os.path.join(TEMP_DIR, file_name)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)