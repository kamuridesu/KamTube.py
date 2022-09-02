import asyncio
from typing import Any, Union
import logging
from sys import stdin
import json
import urllib
import aiohttp

from .util import get, post
from .parsers import urlParse, parse
from .exceptions import *


class KamTube:
    def __init__(self, mode: str="script", debug: bool=False) -> None:
        self.session = aiohttp.ClientSession()
        self.cli = True if mode == "cli" else False
        self.debug = debug
        self.base_api_url = "https://invidious.namazso.eu/api/v1/"
        self.video_html_page = "https://ytb.trom.tf/watch?v="
        self.download_endpoint = "https://ytb.trom.tf/download"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename="kamtube.log")
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        self.logger.debug("Entering context")
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, tb):
        if self.session:
            self.logger.debug("Exit context")
            await self.session.__aexit__(exc_type, exc_val, tb)

    def cli_log(self, message: str) -> None:
        if self.cli:
            print(message, flush=True, file=stdin)  

    async def search(self, query: str, page: int=1, date: str="", sort_by: str="", duration: int=0, _type: str="video", region: str="US") -> Union[dict, list]:
        date = f"&date={date}" if date else ""
        duration = f"duration={duration}" if duration != 0 else ""
        full_query = f"search?q={query}&page={page}&sort_by={sort_by}{duration}{date}&type={_type}&region={region}"
        self.logger.debug(full_query)
        return json.loads((await get(self.session, self.base_api_url + full_query)).decode("utf-8"))

    async def getMediaMetadata(self, media_id: str) -> Union[dict, list]:
        media_id = urlParse(media_id)
        result =  (await get(self.session, self.base_api_url + f"videos/{media_id}")).decode("utf-8")
        if "error" in result:
            try:
                json_error = json.loads(result)['error']
                self.logger.error("Error while retrieving " + self.base_api_url + f"videos/{media_id}: " + json_error)
                raise FileNotFoundError(json_error)
            except json.JSONDecodeError:
                raise UnknownFileError
        else:
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                self.logger.error("Error parsing json data! Data is: " + result)
                raise UnknownFileError

    async def getMediaInfo(self, media_id: str) -> dict[str, Union[str, list]]:
        media_id = urlParse(media_id)
        data = (await get(self.session, self.video_html_page + media_id)).decode("utf-8")
        return parse(data)

    async def getThumbnail(self, media_id: str, quality: str="maxres") -> str:
        media_id = urlParse(media_id)
        data = await self.getMediaMetadata(media_id)
        for q in data['videoThumbnails']:
            if q['quality'] == quality:
                return q['url']

    async def processDownloadBody(self, media_id: str, media_type: str, quality: Union[None, int, float]) -> dict[str, Any]:
        if media_type == "subs":
            raise NotImplemented("Subs are not implemented yet!")
        if media_type not in ["mixed", "video", "audio", "subs"]:
            raise TypeError("Media type can only be 'mixed', 'video', 'audio' or 'subs'")
        data = (await self.getMediaInfo(media_id))
        available_qualities_infos = data[media_type]
        if quality is None and media_type != "subs":
            quality = max([x['quality'] for x in available_qualities_infos])
        for item in available_qualities_infos:
            if item['quality'] == quality:
                return {
                    "id": media_id,
                    "title": data['title'],
                    "query": item['query'],
                    "extension": item['extension']
                }
        self.logger.error("Cannot process download body! Please, check the parameters")
        raise Exception("Cannot process download body! Please, check the parameters")

    async def download(self, media_id: str, media_type: str="mixed", quality: Union[None, int, float]=None) -> dict[str, Union[str, bytes]]:
        body = await self.processDownloadBody(media_id, media_type, quality)
        headers = {
            "Accept": "*/*",
            "DNT": "1",
            "Upgrade-Insecure-Request": "1",
            "Content-type": "application/x-www-form-urlencoded"
        }
        body_query: str = urllib.parse.quote(f"id={body['id']}&title={body['title']}&download_widget=", safe='~@#$&()*!+=:;,?/\'') + urllib.parse.quote(body['query'], safe='~()*!\'')
        self.logger.info("Downloading media " + body['title'] + " with query " + body_query)
        try:
            _bytes = await post(self.session, self.download_endpoint, data=body_query, headers=headers, is_cli=self.cli, title=body['title'])
            if _bytes:
                if self.cli:
                    await self.close() # Closing session on CLI to avoid hanging session object
                return {
                    "title": body['title'],
                    "extension": body['extension'],
                    "bytes": _bytes
                }
        except Exception as e:
            self.logger.error("Download failed! Reason may be something from " + str(e.__class__))
            raise
    
    async def save(self, media_id: str, media_type: str="mixed", quality: Union[None, int, float]=None) -> str:
        response: dict[str, Union[str, bytes]] = await self.download(media_id, media_type, quality)
        extension = response['extension']
        if media_type == "audio":
            extension = "mp3"
        filename = f"{response['title'].replace('/', '-').replace('|', '')}.{extension}"
        self.logger.debug("Saving " + filename)
        with open(filename, "wb") as file:
            file.write(response['bytes'])
        return response['title']

    async def close(self):
        if self.session:
            await self.session.close()
