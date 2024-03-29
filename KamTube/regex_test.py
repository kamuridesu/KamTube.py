from .parsers import urlParse
import unittest


class TestingParsers(unittest.TestCase):
    def testUrlParser(self):
        urls = [
            "http://www.youtube.com/watch?v=cKZDdG9FTKY&feature=channel",
            "http://www.youtube.com/watch?v=yZ-K7nCVnBI&playnext_from=TL&videos=osPknwzXEas&feature=sub",
            "http://youtu.be/6dwqZw0j_jY",
            "http://www.youtube.com/watch?v=6dwqZw0j_jY&feature=youtu.be",
            "http://www.youtube.com/watch?v=yZ-K7nCVnBI&playnext_from=TL&videos=osPknwzXEas&feature=sub",
            "http://www.youtube.com/embed/nas1rJpm7wY?rel=0",
            "http://www.youtube.com/watch?v=peFZbP64dsU",
            "http://youtube.com/v/dQw4w9WgXcQ?feature=youtube_gdata_player",
            "http://youtube.com/watch?v=dQw4w9WgXcQ&feature=youtube_gdata_player",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtube_gdata_player",
            "http://youtu.be/afa-5HQHiAs",
            "http://youtu.be/dQw4w9WgXcQ?feature=youtube_gdata_player",
            "//www.youtube-nocookie.com/embed/up_lNV-yoK4?rel=0",
            "http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo",
            "http://www.youtube.com/ytscreeningroom?v=NRHVzbJVx8I",
            "http://www.youtube.com/user/SilkRoadTheatre#p/a/u/2/6dwqZw0j_jY",
            "http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo?rel=0",
            "http://www.youtube.com/watch?v=cKZDdG9FTKY&feature=channel",
            "http://www.youtube.com/ytscreeningroom?v=NRHVzbJVx8I",
            "http://youtube.com/vi/dQw4w9WgXcQ?feature=youtube_gdata_player",
            "http://youtube.com/?v=dQw4w9WgXcQ&feature=youtube_gdata_player",
            "http://youtube.com/?vi=dQw4w9WgXcQ&feature=youtube_gdata_player",
            "http://youtube.com/watch?vi=dQw4w9WgXcQ&feature=youtube_gdata_player",
        ]
        for url in urls:
            self.assertNotEqual(urlParse(url), None)
