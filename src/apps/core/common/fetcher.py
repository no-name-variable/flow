import time
from typing import Optional, Dict

import aiohttp

from config import get_logger

logger = get_logger(__name__)


class AsyncRESTFetcher:
    _timeout: int = 100
    _params: Optional[Dict[str, str]] = None
    _raise_for_status: bool = False
    _raw_response: bool = False

    def _get_headers(self, **kwargs) -> Optional[Dict]:
        if kwargs:
            return kwargs
        return None

    async def _set_history(self, session, context, params):
        ...

    @classmethod
    async def _params_request(cls, json: dict = None, data: dict = None):
        if json:
            return {
                "json": json
            }
        if data:
            return {
                "data": data
            }
        else:
            return None

    async def _handle_response(self, response: aiohttp.ClientResponse, **kwargs):
        try:
            if self._raw_response:
                return await response.text()

            return await response.json()
        except Exception as exc:
            return await response.text()

    async def _request(
            self,
            url: str,
            method: str = 'GET',
            json: dict = None,
            data: dict = None,
            **kwargs
    ):
        start_time = time.time()

        try:
            request_payload = await self._params_request(json, data) if json or data else {}
            async with aiohttp.ClientSession() as async_session:
                async with async_session.request(
                        method,
                        url,
                        verify_ssl=False,
                        headers=self._get_headers(**kwargs),
                        raise_for_status=True,
                        **request_payload

                ) as response:
                    data = await self._handle_response(response)
                    logger.info(
                        f'Response from {url}, method: {method}, runtime: {time.time() - start_time}'
                    )
                    return data

        except aiohttp.ClientResponseError as e:
            logger.warning(f'Error fetching from url: {url}, error: {e}')
