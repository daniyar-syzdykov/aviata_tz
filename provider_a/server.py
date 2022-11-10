import asyncio
from fastapi import FastAPI
from schemas import SearchSchema
from parse_json import search_in_files
import uvicorn

app = FastAPI()


@app.post('/search')
async def search(data: SearchSchema):
    result = await search_in_files(data)
    await asyncio.sleep(40)
    return result


if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0',
                port=9001, timeout_keep_alive=60)
