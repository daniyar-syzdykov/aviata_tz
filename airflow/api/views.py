import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from database import SearchResult
from database.session import get_session
from .logic.search import search_and_save_results
from .logic.currency import convert_result_curency
from .schemas import SearchSchema, SearchResutlSchema

router = APIRouter()


@router.get('/results/{search_id}/{currency}')
async def get_search_results(search_id: str, currency: str, session=Depends(get_session)):
    db_result: SearchResult = await SearchResult.get_by_search_id(search_id, session)

    if not db_result:
        raise HTTPException(status_code=404, detail="Dosn't exist")

    status = 'COMPLETED' if db_result.status else 'PENDING'
    result = SearchResutlSchema.from_orm(db_result)
    result = await convert_result_curency(search_results=result.dict(), currency=currency)
    return {'search_id': search_id, 'status': status, 'items': result}


@router.post('/search')
async def search_in_providers(tasks: BackgroundTasks, data: SearchSchema, session=Depends(get_session)):
    new_search_result: SearchResult = await SearchResult.create(session=session)
    providers = ['a', 'b']
    for provider in providers:
        tasks.add_task(search_and_save_results,
                       provider=provider,
                       search_query=data.dict(),
                       search_result=new_search_result,
                       session=session)

    return {'search_id': new_search_result.search_id}
