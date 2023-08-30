import scrapy


class MatchFixturesSpiderSpider(scrapy.Spider):
    name = "match_fixtures_spider"
    allowed_domains = ["nerdytips.com"]
    start_urls = ["https://nerdytips.com/all-matches"]

    def parse(self, response):
        matches = response.css(
            '.nt-matches-list-item tbody tr')
        data = {
            "id": 1,
            "platform": {
                "name": "nerdytips",
                "url": "nerdytips.com",
                "matches": []
            }
        }
        for i in range(len(matches)):
            res = ''
            for score in matches[i].css(".score-result span"):
                res += score.css('span::text').get()
            yield {
                "home": matches[i].css(".score-left span::text").get(),
                "away": matches[i].css(".score-right span::text").get(),
                "score_result": res,
                "kickoff": matches[i].css(".score-time::text").get(),
                "tip": f'{matches[i].css(".td-best-tips p::text").get()} {matches[i].css(".td-trust::text").get()}{matches[i].css(".td-trust a::text").get()}',
                "platform": "nerdytips",
            }
