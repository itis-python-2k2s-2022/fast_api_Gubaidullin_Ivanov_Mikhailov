import asyncio

from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services import get_atms, compare_dicts

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data_old = get_atms()
    iteration = 0  # Для демонстрации
    while True:
        data_new = get_atms()
        # changes = compare_dicts(data_new, data_old)  # основной вариант

        if iteration % 2 == 1:  # чтобы продемонстрировать оповещения об обновлении
            changes = compare_dicts({"points": []}, data_old)  # добавляет все в удаленные
        elif iteration % 2 == 0:
            changes = compare_dicts(data_new, {"points": []})  # добавляет все в только появившиеся
        iteration += 1

        if changes:
            data_new["changes"] = changes
            data_old = data_new
        await websocket.send_json(data=data_new)
        # await asyncio.sleep(300)  # основной вариант
        await asyncio.sleep(10)  # чтобы не ждать 100500 часов
