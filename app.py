import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ==========================================
# БАЗА КАРТ (Прямые и Перевернутые значения)
# ==========================================
TAROT_DECK = {
    "Шут": {
        "up": "Начало нового пути. Спонтанность, риск, свобода.",
        "rev": "Необдуманные поступки, страх сделать шаг, глупость."
    },
    "Маг": {
        "up": "Воля, мастерство, проявление. Ты управляешь ситуацией.",
        "rev": "Манипуляции, обман, отсутствие ресурсов или сил."
    },
    "Верховная Жрица": {
        "up": "Интуиция, тайна, скрытые знания. Действуй из тени.",
        "rev": "Игнорирование интуиции, обман, поверхностность."
    },
    "Императрица": {
        "up": "Плодородие, творчество, изобилие. Забота и рост.",
        "rev": "Застой, материальные трудности, отсутствие заботы."
    },
    "Император": {
        "up": "Власть, структура, контроль. Дисциплина и порядок.",
        "rev": "Тирания, слабость, потеря контроля или авторитета."
    },
    "Иерофант": {
        "up": "Традиции, обучение, наставник. Следуй правилам.",
        "rev": "Догмы, бунт, плохой совет, отказ от обучения."
    },
    "Влюбленные": {
        "up": "Выбор, союз, притяжение. Важное решение сердцем.",
        "rev": "Разлад, неверный выбор, дисбаланс в отношениях."
    },
    "Колесница": {
        "up": "Победа, воля, движение вперед. Контроль над эмоциями.",
        "rev": "Потеря контроля, срыв планов, агрессия."
    },
    "Сила": {
        "up": "Смелость, терпение, внутренняя сила. Укрощение страстей.",
        "rev": "Слабость, страхи, подавленные эмоции."
    },
    "Отшельник": {
        "up": "Уединение, поиск истины. Время подумать.",
        "rev": "Изоляция, одиночество, отказ от помощи."
    },
    "Колесо Фортуны": {
        "up": "Судьба, циклы, перемены. Удача на твоей стороне.",
        "rev": "Неудачный период, сопротивление переменам."
    },
    "Справедливость": {
        "up": "Правосудие, баланс, карма. Получишь по заслугам.",
        "rev": "Несправедливость, обман, дисбаланс."
    },
    "Повешенный": {
        "up": "Жертва, пауза, смена перспективы. Отпусти контроль.",
        "rev": "Тупик, бесполезные жертвы, затягивание."
    },
    "Смерть": {
        "up": "Конец, трансформация. Старое уходит, новое приходит.",
        "rev": "Застой, страх перемен, нежелание отпускать."
    },
    "Умеренность": {
        "up": "Баланс, гармония, исцеление. Найди золотую середину.",
        "rev": "Дисбаланс, крайности, нетерпение."
    },
    "Дьявол": {
        "up": "Зависимость, соблазн, материализм. Ты в ловушке.",
        "rev": "Освобождение от оков, но ценой боли."
    },
    "Башня": {
        "up": "Разрушение, кризис. Внезапные перемены рушат планы.",
        "rev": "Страх катастрофы, затяжной кризис."
    },
    "Звезда": {
        "up": "Надежда, вдохновение, вера. Исцеление после кризиса.",
        "rev": "Потеря веры, разочарование, оторванность от реальности."
    },
    "Луна": {
        "up": "Страхи, иллюзии, обман. Не всё то золото, что блестит.",
        "rev": "Раскрытие тайн, выход из иллюзий, тревога."
    },
    "Солнце": {
        "up": "Радость, успех, ясность. Триумф и жизненная сила.",
        "rev": "Временные неудачи, недостаток уверенности."
    },
    "Суд": {
        "up": "Возрождение, пробуждение. Зов судьбы, расплата.",
        "rev": "Страх суда, отказ от прошлого, застой."
    },
    "Мир": {
        "up": "Завершение, гармония, целостность. Успех в начинании.",
        "rev": "Незавершенность, отсутствие финала, пустота."
    },
    "Туз Жезлов": {"up": "Вспышка энергии, новый импульс.", "rev": "Задержка, потеря вдохновения."},
    "Двойка Жезлов": {"up": "Планирование, выбор пути.", "rev": "Страх выбора, отсутствие плана."},
    "Тройка Жезлов": {"up": "Расширение, ожидание результата.", "rev": "Задержки, разочарование в планах."},
    "Четверка Жезлов": {"up": "Праздник, гармония, стабильность.", "rev": "Нестабильность в доме, отмена праздника."},
    "Пятерка Жезлов": {"up": "Конфликт, конкуренция.", "rev": "Избегание конфликта, внутренняя борьба."},
    "Шестерка Жезлов": {"up": "Победа, признание, успех.", "rev": "Падение, отсутствие признания."},
    "Семерка Жезлов": {"up": "Защита, отстаивание позиции.", "rev": "Сдача позиций, усталость от борьбы."},
    "Восьмерка Жезлов": {"up": "Скорость, новости.", "rev": "Задержки, плохие новости."},
    "Девятка Жезлов": {"up": "Стойкость, оборона.", "rev": "Паранойя, истощение."},
    "Десятка Жезлов": {"up": "Перегрузка, ноша.", "rev": "Сброс ноши, освобождение."},
    "Паж Жезлов": {"up": "Новости, вдохновение.", "rev": "Плохие новости, лень."},
    "Рыцарь Жезлов": {"up": "Действие, страсть.", "rev": "Импульсивность, срыв планов."},
    "Королева Жезлов": {"up": "Уверенность, харизма.", "rev": "Ревность, эгоизм."},
    "Король Жезлов": {"up": "Лидерство, амбиции.", "rev": "Деспотизм, высокомерие."},
    "Туз Кубков": {"up": "Любовь, новые эмоции.", "rev": "Эмоциональная пустота, блок."},
    "Двойка Кубков": {"up": "Союз, партнерство.", "rev": "Разлад, недопонимание."},
    "Тройка Кубков": {"up": "Праздник, дружба.", "rev": "Сплетни, ссора в компании."},
    "Четверка Кубков": {"up": "Апатия, скука.", "rev": "Новые возможности, интерес."},
    "Пятерка Кубков": {"up": "Потери, печаль.", "rev": "Принятие, исцеление."},
    "Шестерка Кубков": {"up": "Ностальгия, прошлое.", "rev": "Застревание в прошлом."},
    "Семерка Кубков": {"up": "Иллюзии, выбор.", "rev": "Прояснение, реализм."},
    "Восьмерка Кубков": {"up": "Уход, поиск смысла.", "rev": "Страх уйти, возвращение."},
    "Девятка Кубков": {"up": "Удовлетворение.", "rev": "Неудовлетворенность."},
    "Десятка Кубков": {"up": "Гармония в семье.", "rev": "Семейный разлад."},
    "Паж Кубков": {"up": "Творчество, романтика.", "rev": "Эмоциональная незрелость."},
    "Рыцарь Кубков": {"up": "Романтика, предложение.", "rev": "Ложные обещания."},
    "Королева Кубков": {"up": "Интуиция, забота.", "rev": "Истеричность, зависимость."},
    "Король Кубков": {"up": "Мудрость, баланс.", "rev": "Эмоциональный холод."},
    "Туз Мечей": {"up": "Правда, ясность.", "rev": "Ложь, путаница."},
    "Двойка Мечей": {"up": "Тупик, выбор.", "rev": "Слом блокировки, решение."},
    "Тройка Мечей": {"up": "Боль, разрыв.", "rev": "Заживление ран."},
    "Четверка Мечей": {"up": "Отдых, изоляция.", "rev": "Выход из изоляции."},
    "Пятерка Мечей": {"up": "Поражение, конфликт.", "rev": "Примирение."},
    "Шестерка Мечей": {"up": "Переход, путешествие.", "rev": "Задержка в пути."},
    "Семерка Мечей": {"up": "Обман, хитрость.", "rev": "Раскрытие обмана."},
    "Восьмерка Мечей": {"up": "Ограничения, ловушка.", "rev": "Освобождение."},
    "Девятка Мечей": {"up": "Кошмары, тревога.", "rev": "Выход из депрессии."},
    "Десятка Мечей": {"up": "Конец, дно.", "rev": "Возрождение."},
    "Паж Мечей": {"up": "Любопытство.", "rev": "Сплетни, пустая болтовня."},
    "Рыцарь Мечей": {"up": "Атака, скорость.", "rev": "Агрессия, срыв."},
    "Королева Мечей": {"up": "Логика, холод.", "rev": "Жестокость."},
    "Король Мечей": {"up": "Авторитет, интеллект.", "rev": "Тирания, манипуляции."},
    "Туз Пентаклей": {"up": "Деньги, ресурс.", "rev": "Упущенная выгода."},
    "Двойка Пентаклей": {"up": "Баланс, гибкость.", "rev": "Перегрузка, хаос."},
    "Тройка Пентаклей": {"up": "Командная работа.", "rev": "Отсутствие командного духа."},
    "Четверка Пентаклей": {"up": "Стабильность, контроль.", "rev": "Жадность, потери."},
    "Пятерка Пентаклей": {"up": "Бедность, нужда.", "rev": "Выход из нужды."},
    "Шестерка Пентаклей": {"up": "Щедрость, помощь.", "rev": "Долги, неравенство."},
    "Семерка Пентаклей": {"up": "Ожидание, терпение.", "rev": "Нетерпение, пустая трата."},
    "Восьмерка Пентаклей": {"up": "Труд, мастерство.", "rev": "Лень, халтура."},
    "Девятка Пентаклей": {"up": "Роскошь, успех.", "rev": "Финансовые потери."},
    "Десятка Пентаклей": {"up": "Богатство, наследство.", "rev": "Семейные конфликты из-за денег."},
    "Паж Пентаклей": {"up": "Обучение, старт.", "rev": "Лень, отсутствие мотивации."},
    "Рыцарь Пентаклей": {"up": "Надежность, упорство.", "rev": "Застой, скука."},
    "Королева Пентаклей": {"up": "Забота, уют.", "rev": "Финансовая зависимость."},
    "Король Пентаклей": {"up": "Богатство, стабильность.", "rev": "Скупость, коррупция."}
}

# ==========================================
# HTML ИНТЕРФЕЙС (С общим анализом)
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
        body { background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; background-image: radial-gradient(circle at 50% 0%, rgba(88, 28, 135, 0.4) 0%, transparent 60%); }
        
        .screen { width: 100%; min-height: 100vh; padding: 30px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 0.4s ease; }
        .hidden { display: none !important; opacity: 0; }
        
        h1 { font-size: 30px; text-align: center; margin-bottom: 10px; background: linear-gradient(to right, #c084fc, #e879f9, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p.sub { color: #9ca3af; text-align: center; margin-bottom: 30px; font-size: 15px; }
        
        .btn { background: linear-gradient(135deg, #9333ea, #6b21a8); color: white; border: 2px solid #c084fc; padding: 16px; border-radius: 16px; font-size: 16px; font-weight: 800; width: 100%; max-width: 350px; cursor: pointer; margin-top: 15px; }
        .btn:active { transform: scale(0.95); }
        
        .input-field { width: 100%; max-width: 350px; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(192, 132, 252, 0.3); color: white; font-size: 16px; margin-bottom: 15px; outline: none; resize: none; }
        .input-field:focus { border-color: #c084fc; }
        
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; max-width: 400px; perspective: 1000px; margin-top: 20px;}
        .card-slot { aspect-ratio: 2/3; background: var(--card-bg); border: 1px solid rgba(192, 132, 252, 0.3); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: inset 0 0 15px rgba(0,0,0,0.5); transition: 0.3s; opacity: 0; transform: scale(0.8); }
        .card-slot.revealed { opacity: 1; transform: scale(1); border-color: #c084fc; box-shadow: 0 0 15px #c084fc; }
        
        #results { width: 100%; max-width: 400px; display: flex; flex-direction: column; gap: 15px; margin-top: 20px;}
        .result-card { background: rgba(23, 17, 36, 0.9); border-radius: 16px; padding: 20px; border-left: 5px solid #c084fc; animation: slideUp 0.5s forwards; opacity: 0; transform: translateY(20px); }
        .result-card.rev { border-left-color: #f43f5e; }
        .result-card h4 { font-size: 18px; margin-bottom: 8px; color: #fff; display: flex; justify-content: space-between; }
        .result-card h4 span { font-size: 12px; color: #9ca3af; font-weight: normal; }
        .result-card p { font-size: 14px; color: #9ca3af; line-height: 1.5; }
        
        /* Блок общего вывода */
        .summary-box { background: linear-gradient(135deg, rgba(147, 51, 234, 0.2), rgba(107, 33, 168, 0.2)); border: 1px solid #c084fc; border-radius: 16px; padding: 20px; margin-top: 20px; width: 100%; max-width: 400px; }
        .summary-box h3 { color: #c084fc; font-size: 16px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; text-align: center; }
        .summary-box p { font-size: 15px; color: #f3f4f6; line-height: 1.6; }
        
        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <!-- ЭКРАН 1 -->
    <div id="screen-1" class="screen">
        <h1>Таро Про</h1>
        <p class="sub">Опиши свою ситуацию. Карты укажут на скрытые причины.</p>
        
        <textarea id="user-question" class="input-field" rows="3" placeholder="Например: Почему мне не платят больше?"></textarea>
        
        <p class="sub" style="margin-top: 10px;">Сколько карт вытянуть?</p>
        <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(1)">1</button>
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(3)">3</button>
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(5)">5</button>
            <button class="btn" style="padding: 10px; width: auto; margin-top: 0;" onclick="startReading(8)">8</button>
        </div>
    </div>

    <!-- ЭКРАН 2 -->
    <div id="screen-2" class="screen hidden">
        <h1>Карты тасуются...</h1>
        <p class="sub">Вселенная слушает твой вопрос</p>
        <div class="grid" id="grid"></div>
    </div>

    <!-- ЭКРАН 3 -->
    <div id="screen-3" class="screen hidden">
        <h1>Твой расклад</h1>
        <div id="results"></div>
        <div id="summary" class="summary-box hidden">
            <h3>💡 Общий анализ</h3>
            <p id="summary-text"></p>
        </div>
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
            if(!userQuestion) { alert("Напиши свой вопрос!"); return; }
            
            totalCards = count;
            document.getElementById('screen-1').classList.add('hidden');
            document.getElementById('screen-2').classList.remove('hidden');
            
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            for(let i=0; i<totalCards; i++) {
                let c = document.createElement('div');
                c.className = 'card-slot';
                c.id = `card-${i}`;
                c.innerHTML = '🌌';
                grid.appendChild(c);
            }
            setTimeout(getResult, 1500);
        }

        async function getResult() {
            const res = await fetch(`/api/draw?count=${totalCards}`);
            const data = await res.json();
            
            // Анимация открытия
            data.cards.forEach((card, i) => {
                setTimeout(() => {
                    let slot = document.getElementById(`card-${i}`);
                    if(slot) {
                        slot.innerHTML = card.is_reversed ? '🃏🔄' : '🃏';
                        slot.classList.add('revealed');
                        if(navigator.vibrate) navigator.vibrate(30);
                    }
                }, i * 200);
            });

            setTimeout(() => {
                document.getElementById('screen-2').classList.add('hidden');
                document.getElementById('screen-3').classList.remove('hidden');
                
                const container = document.getElementById('results');
                container.innerHTML = '';
                
                data.cards.forEach((card, i) => {
                    let div = document.createElement('div');
                    div.className = 'result-card' + (card.is_reversed ? ' rev' : '');
                    div.style.animationDelay = `${i * 0.1}s`;
                    
                    let posText = card.is_reversed ? '🔄 Перевернутая' : '⬆️ Прямая';
                    
                    div.innerHTML = `
                        <h4>${i+1}. ${card.name} <span>${posText}</span></h4>
                        <p>${card.desc}</p>
                    `;
                    container.appendChild(div);
                });

                // Выводим общий анализ (склеиваем значения карт)
                const summaryBox = document.getElementById('summary');
                const summaryText = document.getElementById('summary-text');
                
                let text = `Ты спросил: «${userQuestion}». `;
                if (totalCards === 1) {
                    text += `Карта ${data.cards[0].name} (${data.cards[0].is_reversed ? 'перевернутая' : 'прямая'}) говорит о том, что ${data.cards[0].desc.toLowerCase()} Это и есть главный ответ на твой вопрос.`;
                } else {
                    text += `Карты показывают, что ситуация начинается с ${data.cards[0].name.toLowerCase()}. `;
                    text += `В середине расклада (${data.cards[1].name.toLowerCase()}) видно, что ${data.cards[1].desc.toLowerCase()} `;
                    text += `А завершает всё ${data.cards[data.cards.length-1].name.toLowerCase()}, что означает: ${data.cards[data.cards.length-1].desc.toLowerCase()} `;
                    text += `Свяжи эти три энергии вместе, и ты поймешь, куда двигаться дальше.`;
                }
                
                summaryText.innerText = text;
                summaryBox.classList.remove('hidden');
            }, totalCards * 200 + 500); 
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def serve_index():
    return HTMLResponse(HTML_CONTENT)

class CardResult(BaseModel):
    name: str
    desc: str
    is_reversed: bool

class DrawResponse(BaseModel):
    cards: List[CardResult]

@app.get("/api/draw", response_model=DrawResponse)
async def draw_cards(count: int = 3):
    count = max(1, min(count, 8))
    deck_list = list(TAROT_DECK.keys())
    random.shuffle(deck_list)
    chosen = deck_list[:count]
    
    result = []
    for card_name in chosen:
        # 30% шанс, что карта перевернутая
        is_rev = random.random() < 0.3 
        desc = TAROT_DECK[card_name]["rev"] if is_rev else TAROT_DECK[card_name]["up"]
        
        result.append(CardResult(
            name=card_name,
            desc=desc,
            is_reversed=is_rev
        ))
        
    return DrawResponse(cards=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
