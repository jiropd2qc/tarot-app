import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>💼 Путь к успеху</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { 
            --bg: #121212; 
            --panel: #1e1e1e; 
            --primary: #ff9800; 
            --success: #4caf50; 
            --danger: #f44336;
            --text: #ffffff; 
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, sans-serif; user-select: none; }
        body { 
            background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; 
            background-image: url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=1000&auto=format&fit=crop'); 
            background-size: cover; background-position: center; 
        }
        .overlay { background: rgba(0,0,0,0.85); min-height: 100vh; display: flex; flex-direction: column; padding: 20px; }
        
        /* Статы */
        .stats { display: flex; justify-content: space-between; background: var(--panel); padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; }
        .stat-item { text-align: center; font-size: 14px; }
        .stat-value { font-size: 18px; font-weight: bold; color: var(--primary); display: block; margin-top: 5px; }

        /* Аватар и текст */
        .character-area { flex: 1; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 20px; }
        .avatar { width: 150px; height: 150px; border-radius: 50%; border: 4px solid var(--primary); background: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Felix&backgroundColor=ffdfbf') center/cover; box-shadow: 0 0 20px rgba(255,152,0,0.3); }
        
        .dialogue-box { background: rgba(30,30,30,0.95); border: 2px solid var(--primary); padding: 20px; border-radius: 16px; margin-bottom: 20px; min-height: 120px; animation: fadeIn 0.3s ease; }
        .dialogue-text { font-size: 16px; line-height: 1.5; }
        
        /* Кнопки действий */
        .choices { display: flex; flex-direction: column; gap: 10px; }
        .btn { background: #2a2a2a; color: white; border: 1px solid #444; padding: 15px; border-radius: 12px; font-size: 15px; cursor: pointer; transition: 0.2s; text-align: left; display: flex; align-items: center; gap: 10px; }
        .btn:hover { background: var(--primary); color: black; border-color: var(--primary); }
        .btn:active { transform: scale(0.98); }
        .btn-icon { font-size: 20px; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="overlay">
        <!-- Экран 1: Начало -->
        <div id="screen-start" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; text-align: center;">
            <h1 style="color: var(--primary); margin-bottom: 10px;">РЕИНКАРНАЦИЯ БЕЗРАБОТНОГО</h1>
            <p style="margin-bottom: 30px; color: #888;">Твоя жизнь на дне. Но у тебя есть второй шанс. Начни свой путь к миллионам.</p>
            <button class="btn" style="width: 100%; justify-content: center;" onclick="startGame()">🚀 Начать новую жизнь</button>
        </div>

        <!-- Экран 2: Игра -->
        <div id="screen-game" style="display: none; flex-direction: column; height: 100%;">
            <div class="stats">
                <div class="stat-item">💰 Деньги<br><span class="stat-value" id="stat-money">0$</span></div>
                <div class="stat-item">⚡ Энергия<br><span class="stat-value" id="stat-energy">100</span></div>
                <div class="stat-item">🧠 Скилл<br><span class="stat-value" id="stat-skill">0</span></div>
            </div>
            
            <div class="character-area">
                <div class="avatar" id="avatar"></div>
            </div>

            <div class="dialogue-box">
                <div class="dialogue-text" id="story-text"></div>
            </div>

            <div class="choices" id="choices-container"></div>
        </div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        tg.setHeaderColor('#121212');

        // Статы игрока
        let stats = { money: 0, energy: 100, skill: 0 };
        let currentDay = 1;

        const storyData = {
            "start": {
                text: "Ты просыпаешься в съемной квартире. На счету ноль. За окном дождь. Твой телефон показывает 5 пропущенных от коллекторов. Что делаешь?",
                choices: [
                    { text: "Полистать TikTok и поныть", icon: "📱", next: "tiktok" },
                    { text: "Открыть ноутбук и учить Python", icon: "💻", next: "learn_python" },
                    { text: "Пойти на завод грузчиком", icon: "🏋️", next: "factory" }
                ]
            },
            "tiktok": {
                text: "Ты потратил 4 часа на просмотр смешных котов. Прогресс: 0. Энергия упала от лежания.",
                choices: [
                    { text: "Понять, что так жить нельзя", icon: "🤦", next: "start" }
                ],
                effect: () => { stats.energy -= 10; }
            },
            "learn_python": {
                text: "Ты открываешь бесплатный курс на YouTube. Пальцы не слушаются, но ты начинаешь понимать, что такое циклы и переменные. Ты чувствуешь, что становишься умнее.",
                choices: [
                    { text: "Продолжить учиться", icon: "📚", next: "learn_python" },
                    { text: "Пойти спать", icon: "🛌", next: "start" }
                ],
                effect: () => { stats.skill += 10; stats.energy -= 20; }
            },
            "factory": {
                text: "Ты таскал мешки 12 часов. Спина отваливается, но в кармане шуршат купюры. Это честный труд.",
                choices: [
                    { text: "Вернуться домой", icon: "🏠", next: "start" }
                ],
                effect: () => { stats.money += 50; stats.energy -= 40; }
            },
            "win": {
                text: "Поздравляю! Ты накопил на первый стартап и стал успешным IT-предпринимателем. Твоя жизнь изменилась навсегда.",
                choices: []
            }
        };

        function updateUI() {
            document.getElementById('stat-money').innerText = stats.money + "$";
            document.getElementById('stat-energy').innerText = stats.energy;
            document.getElementById('stat-skill').innerText = stats.skill;

            // Если накопил на стартап
            if (stats.money >= 1000 && stats.skill >= 50) {
                renderScene("win");
            }
        }

        function renderScene(sceneId) {
            const scene = storyData[sceneId];
            
            // Применяем эффекты (деньги, энергия)
            if (scene.effect) scene.effect();
            updateUI();

            // Анимация печати текста
            const textEl = document.getElementById('story-text');
            textEl.innerText = "";
            let i = 0;
            const txt = scene.text;
            
            function typeWriter() {
                if (i < txt.length) {
                    textEl.innerText += txt.charAt(i);
                    i++;
                    setTimeout(typeWriter, 20);
                }
            }
            typeWriter();

            // Рендерим кнопки
            const container = document.getElementById('choices-container');
            container.innerHTML = '';
            
            scene.choices.forEach(choice => {
                let btn = document.createElement('button');
                btn.className = 'btn';
                btn.innerHTML = `<span class="btn-icon">${choice.icon}</span> ${choice.text}`;
                btn.onclick = () => {
                    if(navigator.vibrate) navigator.vibrate(20);
                    renderScene(choice.next);
                };
                container.appendChild(btn);
            });
        }

        function startGame() {
            document.getElementById('screen-start').style.display = 'none';
            document.getElementById('screen-game').style.display = 'flex';
            renderScene('start');
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def serve_index():
    return HTMLResponse(HTML_CONTENT)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
