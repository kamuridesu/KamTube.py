from KamTube.kamtube import KamTube
import asyncio


downloader = KamTube(debug=True)

loop = asyncio.get_event_loop()
print(loop.run_until_complete(downloader.save("dQw4w9WgXcQ")))