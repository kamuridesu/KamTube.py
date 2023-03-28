#!/bin/python3
# -*- coding: utf-8 -*-

import sys
import asyncio
import datetime
from typing import Union

from .kamtube import KamTube


class CLI:
    def __init__(self, media_type: str = "mixed"):
        self.media_type = media_type
        self.downloader = KamTube("cli")
        self.loop = asyncio.get_event_loop()

    async def search(self, query: str):
        results = await self.downloader.search(query)
        template = "[{id}] - {title} - {duration}"
        results_formatted = "\n".join(
            [
                template.format(
                    id=_id,
                    title=result["title"],
                    duration=str(datetime.timedelta(seconds=result["lengthSeconds"])),
                )
                for _id, result in enumerate(results)
            ]
        )
        return {"text": results_formatted, "results": results}

    async def interactiveSearch(self, query: str):
        results = await self.search(query)
        print(results["text"], flush=True)
        while True:
            try:
                option = int(input("Choose an option >>> "))
                if option < 0 or option > len(results["results"]) - 1:
                    raise ValueError
                quality = await self.qualitySelector(results["results"][option])
                return await self.save(results["results"][option], quality)
            except (ValueError, TypeError):
                print(
                    "Option needs to be a number between 0 and "
                    + str(len(results["results"]) - 1)
                )

    async def qualitySelector(self, result: dict):
        qualities = (await self.downloader.getMediaInfo(result["videoId"]))[
            self.media_type
        ]
        if self.media_type == "video":
            qualities_str = [
                f"[{index}] - Resolution: {quality['quality']};FPS: {quality['fps']}"
                for index, quality in enumerate(qualities)
            ]
        else:
            qualities_str = [
                f"[{index}] - Quality: {quality['quality']}"
                for index, quality in enumerate(qualities)
            ]
        print("\n".join(qualities_str))
        while True:
            try:
                option = int(input("Choose a quality >>> "))
                if option < 0 or option > len(qualities) - 1:
                    raise ValueError
                return qualities[option]["quality"]
            except (ValueError, TypeError):
                print(
                    "Option needs to be a number between 0 and "
                    + str(len(qualities) - 1)
                )

    async def directDownload(self, query: str):
        results = await self.search(query)
        return await self.save(results["results"][0])

    async def save(self, result: dict, quality: Union[int, float, None] = None):
        await self.downloader.save(result["videoId"], self.media_type, quality)


async def argparse():
    args = sys.argv[1:]
    usage = lambda: print(
        "Usage: kamtube [flags] search query\nFlags: \n  -h or --help: Print this message\n  -d or --direct: Direct download (non interactive)\n  -x or --extract: download audio only"
    )
    if not args:
        usage()
        raise SystemExit
    known_flags = ["-x", "--extract", "-d", "--direct", "-h", "--help"]
    extract = "mixed"
    direct = False
    query_args = []
    for arg in args:
        if arg in ["-x", "--extract"]:
            extract = "audio"
        elif arg in ["-d", "--direct"]:
            direct = True
        elif (arg.startswith("-") and arg not in known_flags) or arg in [
            "-h",
            "--help",
        ]:
            usage()
            raise SystemExit
        else:
            query_args.append(arg)
    cli = CLI(extract)
    if direct:
        await cli.directDownload(" ".join(query_args))
        raise SystemExit
    else:
        await cli.interactiveSearch(" ".join(query_args))
        raise SystemExit


def main():
    try:
        loop = asyncio.get_event_loop()
        task = loop.create_task(argparse())
        loop.run_until_complete(asyncio.gather(task))
        loop.run_forever()
    except KeyboardInterrupt:
        print("Cancelled by the user!")
        sys.exit(1)
