from apps.core.common import fetcher


class Request(fetcher.AsyncRESTFetcher):

    async def get(self, url: str, method="GET", json: dict = None, data: dict = None, **kwargs):
        return await self._request(url=url, method=method, json=json, data=data, **kwargs)

    async def post(self, url: str, method="POST", json: dict = None, data: dict = None, **kwargs):
        return await self._request(url, method=method, json=json, data=data, **kwargs)

    async def __call__(self, url: str, method: str = "GET", json: dict = None, data: dict = None, **kwargs):
        return await self._request(url, method=method, json=json, data=data, **kwargs)


async_request = Request()