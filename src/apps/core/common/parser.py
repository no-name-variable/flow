from apps.core.common.request import async_request


class BaseParser:
    def __init__(self):
        self.request = async_request

    async def parse(self, *args, **kwargs):
        raise NotImplemented

