import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ==========================================
# БАЗА КАРТ (78 карт)
# ==========================================
TAROT_DECK = {
    "Шут": "Начало нового пути. Спонтанность, риск, глупость.",
    "Маг": "Воля, мастерство, проявление. Умение управлять ситуацией.",
    "Верховная Жрица": "Интуиция, тайна, скрытые знания. Действие из тени.",
    "Императрица": "Плодородие, творчество, изобилие. Материнская забота.",
    "Император": "Власть, структура, контроль. Отец, авторитет.",
    "Иерофант": "Традиции, обучение, духовный наставник. Догмы.",
    "Влюбленные": "Выбор, союз, притяжение. Нужно сделать выбор.",
    "Колесница": "Победа, воля, движение вперед. Контроль над эмоциями.",
    "Сила": "Смелость, терпение, внутренняя сила. Укрощение страстей.",
    "Отшельник": "Уединение, поиск истины, самоанализ. Уход в себя.",
    "Колесо Фортуны": "Судьба, циклы, перемены. Удача или рок.",
    "Справедливость": "Правосудие, баланс, карма. Ответственность за поступки.",
    "Повешенный": "Жертва, пауза, смена перспективы. Отказ от контроля.",
    "Смерть": "Конец, трансформация, обновление. Смерть старого.",
    "Умеренность": "Баланс, гармония, исцеление. Алхимия души.",
    "Дьявол": "Зависимость, соблазн, материализм. Оковы.",
    "Башня": "Разрушение, кризис, внезапные перемены. Крах иллюзий.",
    "Звезда": "Надежда, вдохновение, вера. Исцеление после кризиса.",
    "Луна": "Страхи, иллюзии, обман. Подсознание, ночные кошмары.",
    "Солнце": "Радость, успех, ясность. Триумф, жизненная сила.",
    "Суд": "Возрождение, пробуждение, расплата. Зов судьбы.",
    "Мир": "Завершение, гармония, целостность. Успех в начинании.",
    "Туз Жезлов": "Вспышка энергии, новый импульс, вдохновение.",
    "Двойка Жезлов": "Планирование, выбор пути, перспективы.",
    "Тройка Жезлов": "Расширение, ожидание результата, дальний горизонт.",
    "Четверка Жезлов": "Праздник, гармония, стабильность в доме.",
    "Пятерка Жезлов": "Конфликт, конкуренция, борьба за место под солнцем.",
    "Шестерка Жезлов": "Победа, признание, успех, триумф.",
    "Семерка Жезлов": "Защита, отстаивание позиции, преодоление препятствий.",
    "Восьмерка Жезлов": "Скорость, новости, стремительное развитие событий.",
    "Девятка Жезлов": "Стойкость, оборона, усталость от борьбы.",
    "Десятка Жезлов": "Перегрузка, ноша, тяжелый труд.",
    "Паж Жезлов": "Новости, вдохновение, начало творческого пути.",
    "Рыцарь Жезлов": "Действие, страсть, необдуманные поступки.",
    "Королева Жезлов": "Уверенность, харизма, независимость.",
    "Король Жезлов": "Лидерство, амбиции, воля к власти.",
    "Туз Кубков": "Любовь, новые эмоции, начало отношений.",
    "Двойка Кубков": "Союз, партнерство, взаимность.",
    "Тройка Кубков": "Праздник, вечеринка, дружба.",
    "Четверка Кубков": "Апатия, скука, упущенные возможности.",
    "Пятерка Кубков": "Потери, печаль, сожаление.",
    "Шестерка Кубков": "Ностальгия, прошлое, детство.",
    "Семерка Кубков": "Иллюзии, мечты, множество выборов.",
    "Восьмерка Кубков": "Уход, отказ от прошлого, поиск смысла.",
    "Девятка Кубков": "Удовлетворение, эмоциональное благополучие.",
    "Десятка Кубков": "Гармония, счастье в семье, идеал.",
    "Паж Кубков": "Творчество, романтичность, мечтательность.",
    "Рыцарь Кубков": "Романтика, предложение, движение к мечте.",
    "Королева Кубков": "Интуиция, эмпатия, забота.",
    "Король Кубков": "Мудрость, эмоциональный баланс, лидерство.",
    "Туз Мечей": "Правда, победа, ясность ума.",
    "Двойка Мечей": "Выбор, тупик, блокировка эмоций.",
    "Тройка Мечей": "Сердечная боль, разрыв, предательство.",
    "Четверка Мечей": "Отдых, восстановление, изоляция.",
    "Пятерка Мечей": "Конфликт, поражение, поражение в борьбе.",
    "Шестерка Мечей": "Переход, путешествие, преодоление трудностей.",
    "Семерка Мечей": "Обман, хитрость, кража.",
    "Восьмерка Мечей": "Ограничения, ловушка, бессилие.",
    "Девятка Мечей": "Кошмары, тревога, страдания.",
    "Десятка Мечей": "Конец, дно, боль, но и облегчение.",
    "Паж Мечей": "Любопытство, новости, сплетни.",
    "Рыцарь Мечей": "Стремительность, агрессия, атака.",
    "Королева Мечей": "Холодность, логика, независимость.",
    "Король Мечей": "Власть, интеллект, авторитет.",
    "Туз Пентаклей": "Новые возможности, деньги, ресурс.",
    "Двойка Пентаклей": "Баланс, гибкость, жонглирование делами.",
    "Тройка Пентаклей": "Командная работа, мастерство, профессия.",
    "Четверка Пентаклей": "Стабильность, скупость, контроль.",
    "Пятерка Пентаклей": "Бедность, потеря, нужда.",
    "Шестерка Пентаклей": "Щедрость, помощь, баланс в деньгах.",
    "Семерка Пентаклей": "Ожидание, оценка, терпение.",
    "Восьмерка Пентаклей": "Усердный труд, обучение, мастерство.",
    "Девятка Пентаклей": "Роскошь, независимость, успех.",
    "Десятка Пентаклей": "Богатство, наследство, стабильность.",
    "Паж Пентаклей": "Новые начинания в бизнесе, обучение.",
    "Рыцарь Пентаклей": "Медленный прогресс, надежность, упорство.",
    "Королева Пентаклей": "Забота, уют, практичность.",
    "Король Пентаклей": "Успех в бизнесе, богатство, стабильность."
}

# ==========================================
# HTML ИНТЕРФЕЙС (Полностью новый)
# ==========================================
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>🔮 Таро Про</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { --bg: #0b0914; --card-bg: #171124; --accent: #c084fc; --text: #f3f4f6; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, sans-serif; }
        body { background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; background-image: radial-gradient(circle at 50% 0%, rgba(88, 28, 135, 0.4) 0%, transparent 60%), radial-gradient(circle at 10% 90%, rgba(168, 85, 247, 0.1) 0%, transparent 40%); }
        
        .screen { width: 100%; min-height: 100vh; padding: 30px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 0.4s ease; }
        .hidden { display: none !important; opacity: 0; }
        
        h1 { font-size: 30px; text-align: center; margin-bottom: 10px; background: linear-gradient(to right, #c084fc, #e879f9, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p.sub { color: #9ca3af; text-align: center; margin-bottom: 30px; font-size: 15px; }
        
        .btn { background: linear-gradient(135deg, #9333ea, #6b21a8); color: white; border: 2px solid #c084fc; padding: 16px; border-radius: 16px; font-size: 16px; font-weight: 800; width: 100%; max-width: 350px; cursor: pointer; box-shadow: 0 0 20px rgba(147, 51, 234, 0.4); margin-top: 15px; }
        .btn:active { transform: scale(0.95); }
        
        .input-field { width: 100%; max-width: 350px; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(192, 132, 252, 0.3); color: white; font-size: 16px; margin-bottom: 15px; outline: none; resize: none; }
        .input-field:focus { border-color: #c084fc; }
        
        /* Сетка карт */
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; max-width: 400px; perspective: 1000px; margin-top: 20px;}
        .card-slot { aspect-ratio: 2/3; background: var(--card-bg); border: 1px solid rgba(192, 132, 252, 0.3); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: inset 0 0 15px rgba(0,0,0,0.5); transition: 0.3s; opacity: 0; transform: scale(0.8); }
        .card-slot.revealed { opacity: 1; transform: scale(1); border-color: #c084fc; box-shadow: 0 0 15px #c084fc; }
        
        /* Результаты */
        #results { width: 100%; max-width: 400px; display: flex; flex-direction: column; gap: 15px; margin-top: 20px;}
        .result-card { background: rgba(23, 17, 36, 0.9); border-radius: 16px; padding: 20px; border-left: 5px solid #c084fc; animation: slideUp 0.5s forwards; opacity: 0; transform: translateY(20px); }
        .result-card h4 { font-size: 18px; margin-bottom: 8px; color: #fff; }
        .result-card p { font-size: 14px; color: #9ca3af; }
        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <!-- ЭКРАН 1: Ввод вопроса -->
    <div id="screen-1" class="screen">
        <h1>Таро Про</h1>
        <p class="sub">Опиши свою ситуацию или задай вопрос, чтобы карты дали точный ответ.</p>
        
        <textarea id="user-question" class="input-field" rows="4" placeholder="Например: Почему я не могу найти работу мечты?"></textarea>
        
        <p class="sub" style="margin-top: 10px;">Сколько карт вытянуть? (от 1 до 8)</p>
        <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(1)">1</button>
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(3)">3</button>
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(5)">5</button>
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(8)">8</button>
        </div>
    </div>

    <!-- ЭКРАН 2: Анимация вытягивания -->
    <div id="screen-2" class="screen hidden">
        <h1>Карты тасуются...</h1>
        <p class="sub">Вселенная слушает твой вопрос</p>
        <div class="grid" id="grid"></div>
    </div>

    <!-- ЭКРАН 3: Результат -->
    <div id="screen-3" class="screen hidden">
        <h1>Твой расклад</h1>
        <div id="results"></div>
        <button class="btn" onclick="location.reload()" style="margin-top: 30px;">🔄 Новый вопрос</button>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        tg.setHeaderColor('#0b0914');
        
        let totalCards = 3;
        let userQuestion = "";

        function startReading(count) {
            userQuestion = document.getElementById('user-question').value.trim();
            if(!userQuestion) {
                alert("Пожалуйста, напиши свой вопрос!");
                return;
            }
            
            totalCards = count;
            
            // Переходим на экран с картами
            document.getElementById('screen-1').classList.add('hidden');
            document.getElementById('screen-2').classList.remove('hidden');
            
            // Создаем пустые слоты (столько, сколько выбрал юзер)
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            for(let i=0; i<totalCards; i++) {
                let c = document.createElement('div');
                c.className = 'card-slot';
                c.id = `card-${i}`;
                c.innerHTML = '🌌';
                grid.appendChild(c);
            }
            
            // Запускаем анимацию "тасовки" (через 1.5 сек открываем)
            setTimeout(getResult, 1500);
        }

        async function getResult() {
            // Делаем запрос к нашему серверу, передаем количество карт
            const res = await fetch(`/api/draw?count=${totalCards}`);
            const data = await res.json();
            
            // Анимация открытия карт по одной
            data.cards.forEach((card, i) => {
                setTimeout(() => {
                    let slot = document.getElementById(`card-${i}`);
                    if(slot) {
                        slot.innerHTML = '🃏';
                        slot.classList.add('revealed');
                        if(navigator.vibrate) navigator.vibrate(30);
                    }
                }, i * 200); // Задержка 0.2 сек между картами
            });

            // Ждем, пока все откроются, и показываем текст
            setTimeout(() => {
                document.getElementById('screen-2').classList.add('hidden');
                document.getElementById('screen-3').classList.remove('hidden');
                
                const container = document.getElementById('results');
                container.innerHTML = '';
                
                data.cards.forEach((card, i) => {
                    let div = document.createElement('div');
                    div.className = 'result-card';
                    div.style.animationDelay = `${i * 0.1}s`;
                    div.innerHTML = `
                        <h4>🃏 ${i+1}. ${card.name}</h4>
                        <p>${card.desc}</p>
                    `;
                    container.appendChild(div);
                });
            }, totalCards * 200 + 500); 
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
    cards: List[Card]

@app.get("/api/draw", response_model=DrawResponse)
async def draw_cards(count: int = 3):
    # Ограничиваем от 1 до 8
    count = max(1, min(count, 8))
    deck_list = list(TAROT_DECK.keys())
    random.shuffle(deck_list)
    chosen = deck_list[:count]
    return DrawResponse(cards=[Card(name=c, desc=TAROT_DECK[c]) for c in chosen])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
