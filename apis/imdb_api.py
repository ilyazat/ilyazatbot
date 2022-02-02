import aiohttp
import typing as tp
from yarl import URL
import pydantic
from pydantic import BaseModel

imdb_url = URL("https://imdb-api.com/")


class IMDbResponseResult(BaseModel):
    id: str = pydantic.Field(...)
    resultType: str = pydantic.Field(...)
    image: str = pydantic.Field(...)
    title: str = pydantic.Field(...)
    description: str = pydantic.Field(...)


class IMDbResponseData(BaseModel):
    searchType: str = pydantic.Field(...)
    expression: str = pydantic.Field(...)
    results: tp.Optional[tp.List[IMDbResponseResult]] = pydantic.Field(None)
    errorMessage: str = pydantic.Field("")


class IMDbMovieInfo(BaseModel):
    id: str = pydantic.Field(...)
    title: str = pydantic.Field(...)
    fullTitle: str = pydantic.Field(...)
    type: str = pydantic.Field(...)
    image: str = pydantic.Field(...)
    plot: str = pydantic.Field(...)
    imDbRating: str = pydantic.Field(...)


class IMDbSession:
    def __init__(self, imdb_token: str, language: str = "en"):
        self._apiKey = imdb_token
        self.language = language

    async def search_by_expression_imdb(self, expression: str) -> tp.Union[IMDbMovieInfo, None]:
        endpoint = imdb_url / self.language / "API" / "Search" / self._apiKey / expression
        async with aiohttp.ClientSession() as session:
            response = await session.get(endpoint, ssl=False)
            raw_movie_info = IMDbResponseData.parse_obj(await response.json())  # only title and description is year
            if not raw_movie_info.results:
                return None
            return await self._get_nice_description_by_imdb_id(title_id=raw_movie_info.results[0].id,
                                                               session=session)

    async def _get_nice_description_by_imdb_id(self, title_id: str, session: aiohttp.ClientSession) \
            -> tp.Union[IMDbMovieInfo, None]:
        endpoint = imdb_url / self.language / "API" / "Title" / self._apiKey / title_id
        response = await session.get(endpoint, ssl=False)
        response_json = await response.json()
        try:
            return IMDbMovieInfo.parse_obj(response_json)
        except pydantic.ValidationError:
            return None
