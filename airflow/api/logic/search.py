import httpx
import asyncio
from database import SearchResult, SearchResultDetail
from api.schemas import SearchSchema


class SearchInProviders:
    @staticmethod
    async def send_post_request(url: str, json_body):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=json_body, timeout=70)
            except Exception as e:
                raise e

        return response

    @staticmethod
    async def search_in_provider_a(data: SearchSchema):
        result = await SearchInProviders.send_post_request('http://127.0.0.1:9001/search', data)
        return result

    @staticmethod
    async def search_in_provider_b(data: SearchSchema):
        result = await SearchInProviders.send_post_request('http://127.0.0.1:9002/search', data)
        return result


async def obtain_results_from_providers(provider: str, search_query):
    tasks = []

    search = getattr(SearchInProviders, f'search_in_provider_{provider}')
    tasks.append(search(search_query))
    search_results = await asyncio.gather(*tasks, return_exceptions=True)

    return [result.json() for result in search_results]


async def update_search_result(search_result: SearchResult, results, session):
    for provider in results:
        for result in provider:
            search_result.details.append(SearchResultDetail(
                search_result_id=search_result.id,
                items=result,
                price=float(result.get('pricing').get('total')),
                currency=(result.get('pricing').get('currency'))),
            )
    session.add(search_result)

    await search_result.update(id=search_result.id, status=True, session=session)


async def search_and_save_results(provider: str, search_query, search_result: SearchResult, session):
    search: SearchResult = await SearchResult.get_by_search_id(
        search_result.search_id, session=session)
    result = await obtain_results_from_providers(provider, search_query)
    await update_search_result(search, result, session)
