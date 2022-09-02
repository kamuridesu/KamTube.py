from bs4 import BeautifulSoup
from typing import Union
import re


def urlParse(url: str) -> str:
    if re.search("^(?:http:\/\/)?youtu\.be", url):
        return re.match("^(?:http:\/\/)?youtu\.be\/(.{11})", url).group(1)
    elif re.search("^(?:(?:http:)?\/\/)?(?:www\.)?youtube(?:-nocookie)?.com", url):
        match = re.match("(?:http:\/\/)?(?:www\.)?youtube\.com.*?v=(.{11})", url)
        if not match:
            match = re.match("(?:vi=|vi?\/|embed\/)(.{11})", url)
        if not match and re.search("user", url):
            match = url.split("/")
            return match[len(match) - 1].split("?")[0]
        return (match or ["", url])[1]
    if not "/" in url:
        return url
    return None


def parse(document: str) -> dict[str, Union[str, list]]:
    soup: BeautifulSoup = BeautifulSoup(document, "html.parser")
    select = soup.find("select")
    title = soup.find("title").text.replace(" - Invidious", "")
    media_informations: dict["str", Union[str, list]] = {
        "title": title,
        "mixed": [],
        "audio": [],
        "video": [],
        "subs": []
    }
    for item in select.find_all("option"):
        if "video only" in item.text:
            splitted = item.text.strip().split(" - ")
            resolution = int(splitted[0].replace("p", ""))
            extension_fps = splitted[1].split(" @ ")
            fps = int(extension_fps[1].replace("fps", ""))
            extension = extension_fps[0].split("/")[1]
            data = {
                "quality": resolution,
                "fps": fps,
                "extension": extension,
                "query": item['value']
            }
            media_informations['video'].append(data)
        elif "audio only" in item.text:
            splitted = item.text.strip().split(" - ")
            extension_quality = splitted[0].split(" @ ")
            extension = extension_quality[0].split("/")[1]
            quality = float(extension_quality[1].replace("k", ""))
            data = {
                "quality": quality,
                "extension": extension,
                "query": item['value']
            }
            media_informations['audio'].append(data)
        elif "Subtitles" in item.text:
            media_informations['subs'].append({
                "language": item.text.strip().split(" - ")[1],
                "query": item['value']
                })
        else:
            splitted = item.text.strip().split(" - ")
            resolution = int(splitted[0].replace("p", ""))
            extension = splitted[1].split("/")[1]
            data = {
                "quality": resolution,
                "extension": extension,
                "query": item['value']
            }
            media_informations['mixed'].append(data)
    return media_informations
