import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>⚔️ Stickman RPG</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, sans-serif; user-select: none; }
        body { background: #1a1a2e; color: #fff; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        
        /* Шапка */
        .header { background: #16213e; padding: 15px; display: flex; justify-content: space-between; border-bottom: 2px solid #e94560; }
        .stat { font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        .hp-bar { width: 120px; height: 12px; background: #000; border-radius: 6px; overflow: hidden; }
        .hp-fill { height: 100%; background: #00ff00; transition: width 0.3s; }
        .hp-fill.enemy { background: #ff0000; }

        /* Арена */
        .arena { flex: 1; display: flex; justify-content: space-around; align-items: center; background: #0f152d; }
        .fighter { font-size: 80px; transition: transform 0.1s; }
        .fighter.hit { transform: scale(0.9) translateY(10px); filter: drop-shadow(0 0 10px red); }
        
        /* Лог */
        .log { height: 120px; background: #000; padding: 10px; overflow-y: auto; font-size: 13px; color: #00ff00; border-top: 2px solid #e94560; }
        
        /* Кнопки */
        .controls { background: #16213e; padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .btn { background: #e94560; color: white; border: none; padding: 18px; border-radius: 12px; font-size: 16px; font-weight: bold; text-transform: uppercase; cursor: pointer; transition: 0.1s; }
        .btn:active { transform: scale(0.95); }
        .btn:disabled { background: #555; color: #888; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="stat">👤 Игрок (<span id="p-lvl">1</span> lvl)</div>
            <div class="stat">HP: <span id="p-hp-txt">100</span>/<span id="p-hp-max">100</span></div>
            <div class="hp-bar"><div class="hp-fill" id="p-hp-bar" style="width: 100%;"></div></div>
        </div>
        <div style="text-align: right;">
            <div class="stat">👹 <span id="e-name">Гоблин</span></div>
            <div class="stat">HP: <span id="e-hp-txt">50</span>/<span id="e-hp-max">50</span></div>
            <div class="hp-bar" style="margin-left: auto;"><div class="hp-fill enemy" id="e-hp-bar" style="width: 100%;"></div></div>
        </div>
    </div>

    <div class="arena">
        <div class="fighter" id="player-avatar">🏃‍♂️</div>
        <div class="fighter" id="enemy-avatar">👹</div>
    </div>

    <div class="log" id="log">Бой начался! Твой ход.</div>

    <div class="controls">
        <button class="btn" id="btn-attack" onclick="attack()">⚔️ Атака</button>
        <button class="btn" id="btn-heal" onclick="heal()">🧪 Зелье (<span id="p-potions">2</span>)</button>
    </div>

    <script>
        // Инициализация Telegram
        const tg = window.Telegram.WebApp;
        if(tg) { tg.expand(); tg.setHeaderColor('#16213e'); }

        // Характеристики
        let player = { hp: 100, maxHp: 100, lvl: 1, dmg: 15, potions: 2 };
        let enemy = { name: "Гоблин", hp: 50, maxHp: 50, dmg: 10 };
        let turn = true;
        let gameOver = false;

        const logEl = document.getElementById('log');

        function log(msg) {
            logEl.innerHTML += `<br>> ${msg}`;
            logEl.scrollTop = logEl.scrollHeight;
        }

        function updateUI() {
            // Игрок
            document.getElementById('p-lvl').innerText = player.lvl;
            document.getElementById('p-hp-txt').innerText = Math.max(0, player.hp);
            document.getElementById('p-hp-max').innerText = player.maxHp;
            document.getElementById('p-hp-bar').style.width = (Math.max(0, player.hp) / player.maxHp * 100) + "%";
            document.getElementById('p-potions').innerText = player.potions;

            // Враг
            document.getElementById('e-name').innerText = enemy.name;
            document.getElementById('e-hp-txt').innerText = Math.max(0, enemy.hp);
            document.getElementById('e-hp-max').innerText = enemy.maxHp;
            document.getElementById('e-hp-bar').style.width = (Math.max(0, enemy.hp) / enemy.maxHp * 100) + "%";

            // Кнопки
            document.getElementById('btn-attack').disabled = !turn || gameOver;
            document.getElementById('btn-heal').disabled = !turn || gameOver || player.potions <= 0;
        }

        function attack() {
            if (!turn || gameOver) return;
            turn = false;

            let dmg = player.dmg + Math.floor(Math.random() * 5);
            enemy.hp -= dmg;
            log(`⚔️ Ты ударил на ${dmg} урона.`);
            
            // Анимация
            let avatar = document.getElementById('enemy-avatar');
            avatar.classList.add('hit');
            setTimeout(() => avatar.classList.remove('hit'), 200);
            
            updateUI();

            if (enemy.hp <= 0) {
                win();
            } else {
                setTimeout(enemyTurn, 1000);
            }
        }

        function enemyTurn() {
            if (gameOver) return;

            let dmg = enemy.dmg + Math.floor(Math.random() * 5);
            player.hp -= dmg;
            log(`👹 ${enemy.name} ударил на ${dmg} урона.`);
            
            // Анимация
            let avatar = document.getElementById('player-avatar');
            avatar.classList.add('hit');
            setTimeout(() => avatar.classList.remove('hit'), 200);
            
            updateUI();

            if (player.hp <= 0) {
                lose();
            } else {
                turn = true;
                log("Твой ход.");
                updateUI();
            }
        }

        function heal() {
            if (!turn || gameOver || player.potions <= 0) return;
            turn = false;
            player.potions--;
            
            let healAmt = 30;
            player.hp = Math.min(player.maxHp, player.hp + healAmt);
            log(`🧪 Ты выпил зелье и восстановил ${healAmt} HP.`);
            updateUI();
            
            setTimeout(enemyTurn, 1000);
        }

        function win() {
            gameOver = true;
            log(`🏆 ПОБЕДА! Ты убил ${enemy.name}.`);
            
            player.lvl++;
            player.maxHp += 20;
            player.hp = player.maxHp;
            player.dmg += 5;
            log(`⭐ УРОВЕНЬ ПОВЫШЕН до ${player.lvl}! Здоровье восстановлено.`);
            
            document.getElementById('enemy-avatar').style.opacity = '0.2';
            
            setTimeout(spawnEnemy, 3000);
        }

        function lose() {
            gameOver = true;
            log(`💀 ТЫ ПОГИБ. Нажми F5, чтобы начать заново.`);
            document.getElementById('player-avatar').style.opacity = '0.2';
        }

        function spawnEnemy() {
            document.getElementById('enemy-avatar').style.opacity = '1';
            document.getElementById('player-avatar').style.opacity = '1';

            const enemies = [
                { name: "Гоблин", hp: 50, dmg: 10, icon: "👹" },
                { name: "Скелет", hp: 80, dmg: 15, icon: "💀" },
                { name: "Орк", hp: 120, dmg: 20, icon: "👺" },
                { name: "Демон", hp: 200, dmg: 30, icon: "😈" }
            ];

            let maxIdx = Math.min(enemies.length - 1, Math.floor(player.lvl / 2));
            let e = enemies[Math.floor(Math.random() * (maxIdx + 1))];
            
            let scale = player.lvl;
            enemy = { 
                name: e.name, 
                maxHp: e.hp * scale, 
                hp: e.hp * scale, 
                dmg: e.dmg + (scale * 2)
            };
            
            document.getElementById('enemy-avatar').innerText = e.icon;
            
            gameOver = false;
            turn = true;
            log(`⚠️ Появился новый враг: ${enemy.name} (Ур. ${player.lvl})`);
            updateUI();
        }

        // Старт
        updateUI();
    </script>
</body>
</html>
"""

@app.get("/")
async def serve_index():
    return HTMLResponse(HTML_CONTENT)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
