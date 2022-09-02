# KamTube.py

Downloads videos from YouTube via Invidious using Python

# Install: 
    python3 -m pip install --user KamTube

# Usage:
## CLI
`python3 -m KamTube [flags] search`

Eg:

`python3 -m KamTube -x -d never gonna give you up` downloads the song directly

## Script
```py
from KamTube import KamTube
import asyncio

async def main():
    async with KamTube() as downloader:
        await downloader.save("dQw4w9WgXcQ")


asyncio.run(main())
```