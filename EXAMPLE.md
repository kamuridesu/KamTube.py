# To be used in CLI
```py
from KamTube import KamTube
import asyncio

downloader = KamTube("cli")
loop = asyncio.get_event_loop()
loop.run_until_complete(downloader.save("dQw4w9WgXcQ"))
```

# To be used by scripts
```py
from KamTube import KamTube
import asyncio

async def main():
    async with KamTube() as downloader:
        await downloader.save("dQw4w9WgXcQ")


asyncio.run(main())
```