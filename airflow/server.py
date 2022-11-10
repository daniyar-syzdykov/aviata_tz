from fastapi import FastAPI
from database.session import create_tables, close_connections
from datetime import datetime
from api.logic.currency import save_conversion_reate
import httpx
from fastapi_utils.tasks import repeat_every
from api.views import router
import uvicorn


app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def start():
    await create_tables()


@app.on_event('startup')
@repeat_every(seconds=60*60*24)
async def update_exchange_rage():
    url = f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={datetime.now().date().strftime("%d.%m.%Y")}'
    async with httpx.AsyncClient() as client:
        resposne = await client.get(url)
        save_conversion_reate(resposne.content.decode('utf8'))


@app.on_event('shutdown')
async def end():
    await close_connections()


if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0',
                port=9000, timeout_keep_alive=60, reload=True)
