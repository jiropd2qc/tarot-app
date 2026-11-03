import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

TAROT_DECK = {
    "Шут": "Начало нового пути. Спонтанность, риск, глупость.",
    "Маг": "Воля, мастерство, проявление. Умение управлять ситуацией.",
    "Верховная Жрица": "Интуиция, тайна, скрытые знания.",
    "Императрица": "Плодородие, творчество, изобилие.",
    "Император": "Власть, структура, контроль.",
    "Иерофант": "Традиции, обучение, духовный наставник.",
    "Влюбленные": "Выбор, союз, притяжение.",
    "Колесница": "Победа, воля, движение вперед.",
    "Сила": "Смелость, терпение, внутренняя сила.",
    "Отшельник": "Уединение, поиск истины, самоанализ.",
    "Колесо Фортуны": "Судьба, циклы, перемены.",
    "Справедливость": "Правосудие, баланс, карма.",
    "Повешенный": "Жертва, пауза, смена перспективы.",
    "Смерть": "Конец, трансформация, обновление.",
    "Умеренность": "Баланс, гармония, исцеление.",
    "Дьявол": "Зависимость, соблазн, материализм.",
    "Башня": "Разрушение, кризис, внезапные перемены.",
    "Звезда": "Надежда, вдохновение, вера.",
    "Луна": "Страхи, иллюзии, обман.",
    "Солнце": "Радость, успех, ясность.",
    "Суд": "Возрождение, пробуждение, расплата.",
    "Мир": "Завершение, гармония, целостность.",
}

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>🔮 Таро</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { --bg: #0b0914; --card-bg: #171124; --accent: #c084fc; --text: #f3f4f6; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, sans-serif; }
        body { background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; background-image: radial-gradient(circle at 50% 0%, rgba(88, 28, 135, 0.4) 0%, transparent 60%), radial-gradient(circle at 10% 90%, rgba(168, 85, 247, 0.1) 0%, transparent 40%); }
        .screen { width: 100%; min-height: 100vh; padding: 30px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 0.4s ease; }
        .hidden { display: none !important; opacity: 0; }
        h1 { font-size: 32px; text-align: center; margin-bottom: 10px; background: linear-gradient(to right, #c084fc, #e879f9, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 10px rgba(192, 132, 252, 0.3)); }
        p.sub { color: #9ca3af; text-align: center; margin-bottom: 40px; font-size: 16px; line-height: 1.5; }
        .btn { background: linear-gradient(135deg, #9333ea, #6b21a8); color: white; border: 2px solid #c084fc; padding: 18px; border-radius: 16px; font-size: 18px; font-weight: 800; width: 100%; max-width: 350px; cursor: pointer; box-shadow: 0 0 20px rgba(147, 51, 234, 0.4); transition: transform 0.1s; }
        .btn:active { transform: scale(0.95); }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; width: 100%; max-width: 400px; perspective: 1000px; }
        .card-slot { aspect-ratio: 2/3; background: var(--card-bg); border: 1px solid rgba(192, 132, 252, 0.3); border-radius: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 28px; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow: inset 0 0 15px rgba(0,0,0,0.5); }
        .card-slot.selected { transform: translateY(-10px) rotateY(15deg); border-color: #c084fc; box-shadow: -5px 5px 20px rgba(192, 132, 252, 0.4); background: #2e1065; }
        #results { width: 100%; max-width: 400px; display: flex; flex-direction: column; gap: 15px; margin-top: 20px;}
        .result-card { background: rgba(23, 17, 36, 0.8); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border-left: 5px solid #c084fc; animation: slideUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; opacity: 0; transform: translateY(30px); }
        .result-card:nth-child(1) { animation-delay: 0.2s; }
        .result-card:nth-child(2) { animation-delay: 0.5s; }
        .result-card:nth-child(3) { animation-delay: 0.8s; }
        .result-card h3 { color: #c084fc; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
        .result-card h4 { font-size: 20px; margin-bottom: 10px; color: #fff; }
        .result-card p { font-size: 15px; color: #9ca3af; line-height: 1.4; }
        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div id="screen-1" class="screen">
        <h1>Тайны Таро</h1>
        <p class="sub">Узнай истинную причину<br>событий в твоей жизни</p>
        <button class="btn" onclick="start()">✨ Начать гадание</button>
    </div>
    <div id="screen-2" class="screen hidden">
        <h1>Выбери карты</h1>
        <p class="sub" id="counter">Выбрано: 0 из 3</p>
        <div class="grid" id="grid"></div>
    </div>
    <div id="screen-3" class="screen hidden">
        <h1>Твой расклад</h1>
        <p class="sub">Вселенная дала ответ</p>
        <div id="results"></div>
        <button class="btn" onclick="location.reload()" style="margin-top: 30px; font-size: 16px;">🔄 Заново</button>
    </div>
    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        tg.setHeaderColor('#0b0914');
        tg.setBackgroundColor('#0b0914');
        let selected = 0;
        function start() {
            document.getElementById('screen-1').classList.add('hidden');
            document.getElementById('screen-2').classList.remove('hidden');
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            selected = 0;
            for(let i=0; i<12; i++) {
                let c = document.createElement('div');
                c.className = 'card-slot';
                c.innerHTML = '🌌';
                c.onclick = () => select(c);
                grid.appendChild(c);
            }
        }
        function select(el) {
            if(el.classList.contains('selected') || selected >= 3) return;
            if(navigator.vibrate) navigator.vibrate(50);
            el.classList.add('selected');
            el.innerHTML = '🌟';
            selected++;
            document.getElementById('counter').innerText = `Выбрано: ${selected} из 3`;
            if(selected === 3) setTimeout(getResult, 600);
        }
        async function getResult() {
            document.getElementById('screen-2').classList.add('hidden');
            document.getElementById('screen-3').classList.remove('hidden');
            const res = await fetch('/api/draw');
            const data = await res.json();
            const labels = ["1️⃣ Корень проблемы", "2️⃣ Текущее состояние", "3️⃣ Скрытая причина"];
            const container = document.getElementById('results');
            container.innerHTML = '';
            data.cards.forEach((card, i) => {
                let div = document.createElement('div');
                div.className = 'result-card';
                div.innerHTML = `<h3>${labels[i]}</h3><h4>🃏 ${card.name}</h4><p>${card.desc}</p>`;
                container.appendChild(div);
            });
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def serve_index():
    return HTMLResponse(HTML_CONTENT)

class Card(BaseModel):
    name: str
    desc: str

class DrawResponse(BaseModel):
    cards: list[Card]

@app.get("/api/draw", response_model=DrawResponse)
async def draw_cards():
    deck_list = list(TAROT_DECK.keys())
    random.shuffle(deck_list)
    chosen = deck_list[:3]
    return DrawResponse(cards=[Card(name=c, desc=TAROT_DECK[c]) for c in chosen])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)