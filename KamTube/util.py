import aiohttp
import asyncio


def progress(count, total, suffix=''):
    length = 40
    filled_len = int(round(length * count / float(total)))
    percents = round(100 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (length - filled_len)
    print('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix), flush=True, end="")


async def get(session: aiohttp.ClientSession, url: str) -> bytes:
    async with session.request("GET", url) as resp:
        return await resp.read()


async def post(session: aiohttp.ClientSession, url: str, data: str, headers: dict={}, is_cli: bool=False, title: str="") -> bytes:
    async with session.request("POST", url, data=data, headers=headers) as resp:
        total_content_length = int(resp.headers.get("Content-Length"))
        buffer = b""
        total_downloaded = 0
        async for raw_data, end_of_http_chunk in resp.content.iter_chunks():
            total_downloaded += len(raw_data)
            if is_cli:
                progress(total_downloaded, total_content_length, title)
            buffer += raw_data
            if not end_of_http_chunk:
                continue
        return buffer


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
