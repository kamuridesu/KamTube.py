import requests
from bs4 import BeautifulSoup
import asyncio
import json
from urllib.parse import quote


class KamTube:
    def __init__(self) -> None:
        self.base_api = "https://invidious.namazso.eu/api/v1/"
        self.ytb_trom_url = "https://ytb.trom.tf/watch?v="
        self.ytb_trom_download_url = "https://ytb.trom.tf/latest_version?download_widget="
    
    async def urlParser(self, url: str) -> str:
        if not url.startswith("https://"):
            url = "https://" + url
        if "youtu.be" in url:
            url = url.split("/")
            id = ""
            if "shorts" in url:
                id = url[4]
            else:
                id = url[3]
            url = id
        elif "youtube.com" in url:
            url = url.replace("youtube.com/watch?=", "")
        url = url.strip("https://")
        return url

    async def fetcher(self, url: str) -> bytes:
        r = requests.get(url)
        return r._content

    async def search(self, query: str, page: int=1, sort_by: str="relevance", date: str="", duration: str="", type: str="video", region: str="US") -> list:
        page = page if page else 1
        sort_by = sort_by if sort_by else "relevance"
        date = "&date=" + date if date else ""
        duration = "&duration" + duration if duration else ""
        type = type if type else "video"
        region = region if region else "US"
        full_query = f"search?q={query}&page={page}&sort_by={sort_by}{date}{duration}&type={type}&region={region}"
        return json.loads(await self.fetcher(self.base_api + full_query))

    async def getFullMetadata(self, video_id: str) -> dict:
        video_id = await self.urlParser(video_id)
        return json.loads(await self.fetcher(self.base_api + f"videos/{video_id}"))

    async def getVideoInfos(self, video_id: str) -> dict:
        video_id = await self.urlParser(video_id)
        data = await self.fetcher(self.ytb_trom_url + video_id)
        soup = BeautifulSoup(data, "html.parser")
        options = soup.findAll("select")[0].findAll("option")
        name = soup.find("title").text.strip(" - Invidious").strip()
        infos = {"title": name, "infos": []}
        for option in options:
            value = option.get("value")
            quality = option.text
            infos["infos"].append({"quality": quality, "urinfo": value})
        return infos

    async def getVideoDownloadUrl(self, video_id: str, quality: str="360") -> dict:
        video_id = await self.urlParser(video_id)
        v_data = await self.getVideoInfos(video_id)
        data = v_data['infos']
        title = v_data['title']
        try:
            for d in data:
                if quality in d["quality"]:
                    return {"title": title, "data": self.ytb_trom_download_url + quote(d["urinfo"])}
        except Exception:
            print("[!] Error while getting download url")
            return None

    async def download(self, video_id: str, quality: str="360") -> dict:
        video_id = await self.urlParser(video_id)
        data = await self.getVideoDownloadUrl(video_id, quality)
        title = data['title']
        url = data['data']
        if url:
            try:
                return {"title": title, "data": requests.get(url).content}
            except Exception:
                print("[!] Error while downloading")
                return None
        else:
            print("[!] Error while getting download url")
            return None

    async def save(self, video_id: str, quality: str="360") -> None:
        video_id = await self.urlParser(video_id)
        data = await self.download(video_id, quality)
        if data:
            try:
                with open(data['title'] + ".mp4", "wb") as f:
                    f.write(data["data"])
                print("[+] Video saved as " + data['title'] + ".mp4")
            except Exception:
                print("[!] Error while saving")
                return None
        else:
            print("[!] Error while downloading")
            return None

    async def getThumbnail(self, video_id: str) -> str:
        video_id = await self.urlParser(video_id)
        data = await self.getFullMetadata(video_id)
        quality = "maxres"
        for d in data['videoThumbnails']:
            if d['quality'] == quality:
                return d['url']
        return None


def main():
    kamtube = KamTube()
    asyncio.run(kamtube.save("HUnnxRicDwM", "audio"))


if __name__ == "__main__":
    main()