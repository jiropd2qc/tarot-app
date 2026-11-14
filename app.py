import asyncio
import os
import json
import random
import uvicorn
import zipfile
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ==========================================
# НАСТРОЙКИ
# ==========================================
BOT_TOKEN = "8839402895:AAE8QTs2uXcg64vi2scRU8R_QlJ9Itu_eCY"
WEB_APP_URL = "https://tarot-app-xxxx.onrender.com" # <--- СЮДА ВСТАВЬ ССЫЛКУ ИЗ RENDER (когда создашь)

app = FastAPI()
DATA_FILE = "data.json"

# База данных в JSON (для теста)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"accounts": [], "proxies": [], "tasks": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==========================================
# HTML ИНТЕРФЕЙС (MINI APP)
# ==========================================
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Управление софтом</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: -apple-system, sans-serif; background: #0f172a; color: #fff; margin: 0; padding: 20px; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; overflow-x: auto; }
        .tab { background: #1e293b; color: #94a3b8; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; white-space: nowrap; }
        .tab.active { background: #38bdf8; color: #000; }
        .panel { display: none; }
        .panel.active { display: block; }
        
        .card { background: #1e293b; padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .card-info { font-size: 14px; line-height: 1.4; }
        .card-info strong { color: #e2e8f0; font-size: 16px; display: block; margin-bottom: 4px; }
        .card-info span { color: #94a3b8; font-size: 12px; }
        
        input, select { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; margin-bottom: 10px; box-sizing: border-box; }
        button.btn { width: 100%; padding: 14px; border-radius: 8px; border: none; background: #38bdf8; color: #000; font-weight: bold; font-size: 16px; cursor: pointer; margin-bottom: 10px; }
        button.del { background: #ef4444; color: white; padding: 8px 12px; border-radius: 6px; border: none; cursor: pointer; }
        .file-input { background: #38bdf8; color: #000; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; cursor: pointer; display: block; margin-bottom: 10px; }
        #file-name { color: #38bdf8; font-size: 12px; text-align: center; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="tabs">
        <div class="tab active" onclick="showTab('accounts', this)">📱 Аккаунты</div>
        <div class="tab" onclick="showTab('proxies', this)">🔗 Прокси</div>
        <div class="tab" onclick="showTab('tasks', this)">🚀 Задачи</div>
    </div>

    <!-- АККАУНТЫ -->
    <div id="panel-accounts" class="panel active">
        <label class="file-input">
            📥 Загрузить ZIP с сессиями
            <input type="file" id="zipFile" accept=".zip" onchange="uploadZip()" style="display:none;">
        </label>
        <div id="file-name"></div>
        <div id="accounts-list"></div>
    </div>

    <!-- ПРОКСИ -->
    <div id="panel-proxies" class="panel">
        <input type="text" id="proxyInput" placeholder="host:port:user:pass">
        <button class="btn" onclick="addProxy()">➕ Добавить прокси</button>
        <div id="proxies-list"></div>
    </div>

    <!-- ЗАДАЧИ -->
    <div id="panel-tasks" class="panel">
        <input type="text" id="taskName" placeholder="Название задачи">
        <input type="text" id="taskMsg" placeholder="Текст сообщения (можно {username})">
        <label class="file-input">
            📄 Загрузить базу (TXT)
            <input type="file" id="baseFile" accept=".txt" onchange="uploadBase()" style="display:none;">
        </label>
        <div id="base-name"></div>
        <button class="btn" onclick="createTask()">✅ Создать задачу</button>
        <div id="tasks-list"></div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        let currentBasePath = "";

        function showTab(name, el) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('panel-' + name).classList.add('active');
            if(name === 'accounts') loadAccounts();
            if(name === 'proxies') loadProxies();
            if(name === 'tasks') loadTasks();
        }

        async function api(path, method='GET', body=null) {
            const opts = { method };
            if (body) {
                opts.headers = {'Content-Type': 'application/json'};
                opts.body = JSON.stringify(body);
            }
            const res = await fetch(path, opts);
            return res.json();
        }

        // --- ПРОКСИ ---
        async function loadProxies() {
            const data = await api('/api/proxies');
            let html = '';
            data.forEach((p, i) => {
                html += `<div class="card"><div class="card-info"><strong>🌍 Прокси #${i+1}</strong><span>${p.addr}</span></div><button class="del" onclick="delProxy(${i})">🗑</button></div>`;
            });
            document.getElementById('proxies-list').innerHTML = html;
        }
        async function addProxy() {
            const addr = document.getElementById('proxyInput').value;
            if(!addr) return;
            await api('/api/proxies', 'POST', {addr});
            document.getElementById('proxyInput').value = '';
            loadProxies();
        }
        async function delProxy(index) {
            await api('/api/proxies/'+index, 'DELETE');
            loadProxies();
        }

        // --- АККАУНТЫ ---
        async function loadAccounts() {
            const data = await api('/api/accounts');
            let html = '';
            data.forEach((a, i) => {
                let proxy = a.proxy ? `🔗 ${a.proxy}` : `❌ Без прокси`;
                html += `<div class="card"><div class="card-info"><strong>📱 ${a.name}</strong><span>${proxy}</span></div></div>`;
            });
            document.getElementById('accounts-list').innerHTML = html;
        }
        async function uploadZip() {
            const file = document.getElementById('zipFile').files[0];
            if(!file) return;
            document.getElementById('file-name').innerText = "Загрузка...";
            const formData = new FormData();
            formData.append("file", file);
            const res = await fetch('/api/accounts/upload', {method: 'POST', body: formData});
            const data = await res.json();
            document.getElementById('file-name').innerText = `✅ Загружено: ${data.added}`;
            loadAccounts();
            tg.HapticFeedback.notificationOccurred('success');
        }

        // --- ЗАДАЧИ ---
        async function loadTasks() {
            const data = await api('/api/tasks');
            let html = '';
            data.forEach((t, i) => {
                html += `<div class="card"><div class="card-info"><strong>🚀 ${t.name}</strong><span>Контактов: ${t.total_contacts} | Статус: ${t.status}</span></div><button class="btn" style="width:auto; padding: 8px; margin:0;" onclick="startTask(${i})">▶️</button></div>`;
            });
            document.getElementById('tasks-list').innerHTML = html;
        }
        async function uploadBase() {
            const file = document.getElementById('baseFile').files[0];
            if(!file) return;
            document.getElementById('base-name').innerText = "Загрузка...";
            const formData = new FormData();
            formData.append("file", file);
            const res = await fetch('/api/tasks/upload_base', {method: 'POST', body: formData});
            const data = await res.json();
            currentBasePath = data.path;
            document.getElementById('base-name').innerText = `✅ База: ${data.count} контактов`;
        }
        async function createTask() {
            const name = document.getElementById('taskName').value;
            const msg = document.getElementById('taskMsg').value;
            if(!name || !msg || !currentBasePath) return alert("Заполни все поля и загрузи базу");
            await api('/api/tasks', 'POST', {name, msg, base: currentBasePath, total_contacts: 0});
            document.getElementById('taskName').value = '';
            document.getElementById('taskMsg').value = '';
            loadTasks();
        }
        async function startTask(index) {
            await api('/api/tasks/'+index+'/start', 'POST');
            alert("Задача запущена в фоне!");
            loadTasks();
        }

        // Инициализация
        loadAccounts();
    </script>
</body>
</html>
"""

# ==========================================
# API СЕРВЕРА
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT

@app.get("/api/proxies")
async def get_proxies():
    return load_data().get("proxies", [])

class ProxyAdd(BaseModel):
    addr: str

@app.post("/api/proxies")
async def add_proxy(req: ProxyAdd):
    data = load_data()
    data["proxies"].append({"addr": req.addr})
    save_data(data)
    return {"ok": True}

@app.delete("/api/proxies/{index}")
async def delete_proxy(index: int):
    data = load_data()
    if 0 <= index < len(data["proxies"]):
        data["proxies"].pop(index)
        save_data(data)
    return {"ok": True}

@app.get("/api/accounts")
async def get_accounts():
    return load_data().get("accounts", [])

@app.post("/api/accounts/upload")
async def upload_accounts(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return JSONResponse({"error": "Нужен ZIP"}, status_code=400)
    
    os.makedirs("sessions", exist_ok=True)
    zip_path = f"sessions/{file.filename}"
    with open(zip_path, "wb") as f:
        f.write(await file.read())
        
    data = load_data()
    added = 0
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if name.endswith(".session"):
                z.extract(name, "sessions")
                fname = os.path.basename(name)
                if any(a["name"] == fname for a in data["accounts"]): continue
                data["accounts"].append({"name": fname, "file": f"sessions/{fname}", "proxy": ""})
                added += 1
    save_data(data)
    os.remove(zip_path)
    return {"added": added}

@app.get("/api/tasks")
async def get_tasks():
    return load_data().get("tasks", [])

@app.post("/api/tasks/upload_base")
async def upload_base(file: UploadFile = File(...)):
    os.makedirs("bases", exist_ok=True)
    path = f"bases/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        count = len([l for l in f if l.strip()])
    return {"path": path, "count": count}

class TaskCreate(BaseModel):
    name: str
    msg: str
    base: str
    total_contacts: int

@app.post("/api/tasks")
async def create_task(req: TaskCreate):
    data = load_data()
    data["tasks"].append({
        "name": req.name, "msg": req.msg, "base": req.base,
        "total_contacts": req.total_contacts, "status": "Ожидание"
    })
    save_data(data)
    return {"ok": True}

@app.post("/api/tasks/{index}/start")
async def start_task(index: int):
    data = load_data()
    if 0 <= index < len(data["tasks"]):
        data["tasks"][index]["status"] = "Работает"
        save_data(data)
        # Здесь в будущем будет запуск Telethon в фоне
        # (пока просто имитация, чтобы не вешать сервер)
    return {"ok": True}

# ==========================================
# ТЕЛЕГРАМ БОТ
# ==========================================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Замени ссылку ниже на ту, что выдаст Render!
    url = "https://tarot-app-xxxx.onrender.com" 
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Открыть систему", web_app=WebAppInfo(url=url))]
    ])
    await message.answer("Привет! Управление аккаунтами и задачами внутри:", reply_markup=kb)

# ==========================================
# ЗАПУСК
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
