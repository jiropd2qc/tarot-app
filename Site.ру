import asyncio
import os
import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ==========================================
# НАСТРОЙКИ
# ==========================================
BOT_TOKEN = "8839402895:AAE8QTs2uXcg64vi2scRU8R_QlJ9Itu_eCY"
WEB_APP_URL = "ССЫЛКА_С_ХОСТИНГА" # <--- СЮДА ВСТАВИШЬ ССЫЛКУ ПОСЛЕ ДЕПЛОЯ

# ==========================================
# ВЕБ-СЕРВЕР (MINI APP)
# ==========================================
app = FastAPI()
DATA_FILE = "proxies.json"

def load_proxies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_proxies(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Прокси Менеджер</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: -apple-system, sans-serif; background: #0f172a; color: #fff; margin: 0; padding: 20px; }
        h2 { text-align: center; color: #38bdf8; margin-bottom: 20px; font-size: 22px; }
        
        /* Стили карточек как на TraffSoft */
        .proxy-card { background: #1e293b; padding: 15px; border-radius: 12px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #334155; transition: 0.2s; }
        .proxy-card:active { background: #2a3a52; }
        .proxy-left { display: flex; align-items: center; gap: 15px; }
        .proxy-icon { background: #38bdf8; color: #000; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .proxy-info { display: flex; flex-direction: column; }
        .proxy-title { font-size: 16px; font-weight: bold; color: #e2e8f0; margin-bottom: 4px; }
        .proxy-addr { font-size: 12px; color: #94a3b8; word-break: break-all; }
        
        .del-btn { background: #ef4444; color: white; border: none; padding: 8px 12px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        
        .input-group { display: flex; gap: 10px; margin-top: 20px; flex-direction: column; }
        input { padding: 15px; border-radius: 10px; border: 1px solid #334155; background: #0f172a; color: white; font-size: 16px; outline: none; }
        button.add-btn { padding: 15px; border-radius: 10px; border: none; background: #38bdf8; color: #000; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.2s; }
        button.add-btn:active { background: #0ea5e9; }
    </style>
</head>
<body>
    <h2>🔗 Управление прокси</h2>
    <div id="proxy-list"></div>
    
    <div class="input-group">
        <input type="text" id="proxyInput" placeholder="host:port:user:pass">
        <button class="add-btn" onclick="addProxy()">➕ Добавить прокси</button>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // Простая имитация флагов по первым буквам или просто дефолтная иконка
        const getFlag = (addr) => {
            if (addr.includes('de')) return '🇩🇪';
            if (addr.includes('us')) return '🇺🇸';
            if (addr.includes('ua')) return '🇺🇦';
            if (addr.includes('se')) return '🇸🇪';
            return '🌐';
        };

        async function loadProxies() {
            const res = await fetch('/api/proxies');
            const data = await res.json();
            const list = document.getElementById('proxy-list');
            list.innerHTML = '';
            
            if(data.length === 0) {
                list.innerHTML = '<p style="text-align:center; color:#64748b;">Список пуст</p>';
                return;
            }

            data.forEach((p, i) => {
                const flag = getFlag(p.addr);
                list.innerHTML += `
                    <div class="proxy-card">
                        <div class="proxy-left">
                            <div class="proxy-icon">${flag}</div>
                            <div class="proxy-info">
                                <div class="proxy-title">Прокси #${i+1}</div>
                                <div class="proxy-addr">${p.addr}</div>
                            </div>
                        </div>
                        <button class="del-btn" onclick="delProxy(${i})">🗑</button>
                    </div>
                `;
            });
        }

        async function addProxy() {
            const addr = document.getElementById('proxyInput').value.trim();
            if(!addr) return alert("Введи прокси");
            
            await fetch('/api/proxies/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ addr: addr })
            });
            
            document.getElementById('proxyInput').value = '';
            loadProxies();
            tg.HapticFeedback.notificationOccurred('success'); // Вибрация при успехе
        }

        async function delProxy(index) {
            await fetch(`/api/proxies/${index}`, { method: 'DELETE' });
            loadProxies();
        }

        loadProxies();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT

@app.get("/api/proxies")
async def get_proxies():
    return load_proxies()

class ProxyAdd(BaseModel):
    addr: str

@app.post("/api/proxies/add")
async def add_proxy(req: ProxyAdd):
    proxies = load_proxies()
    proxies.append({"addr": req.addr})
    save_proxies(proxies)
    return {"ok": True}

@app.delete("/api/proxies/{index}")
async def delete_proxy(index: int):
    proxies = load_proxies()
    if 0 <= index < len(proxies):
        proxies.pop(index)
        save_proxies(proxies)
    return {"ok": True}

# ==========================================
# TELEGRAM БОТ
# ==========================================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Открыть меню прокси", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Привет! Нажми кнопку ниже, чтобы открыть Mini App:", reply_markup=kb)

# ==========================================
# ЗАПУСК
# ==========================================
async def run_web():
    # Для хостинга Render/Railway ОБЯЗАТЕЛЬНО нужен порт из переменной окружения $PORT
    port = int(os.environ.get("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    print(f"🚀 Бот и Сайт запущены!")
    await asyncio.gather(
        dp.start_polling(bot),
        run_web()
    )

if __name__ == "__main__":
    asyncio.run(main())
