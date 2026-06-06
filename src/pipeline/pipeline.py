from src.web.fetcher import WebsiteFetcher

from src.verification.engineering import EngineeringVerifier

from src.verification.mba import MBAVerifier

from src.verification.phd import PhDVerifier
from src.web.crawler import WebsiteCrawler
from src.verification.age import AgeVerifier
from src.collectors.leadership_collector import LeadershipCollector
from src.collectors.address_collector import AddressCollector

class VerificationPipeline:

    def __init__(self):

        self.fetcher = WebsiteFetcher()

        self.engineering = EngineeringVerifier()

        self.mba = MBAVerifier()

        self.phd = PhDVerifier()
        self.age = AgeVerifier()
        self.crawler = WebsiteCrawler()

    def run(self, url):

        text = self.crawler.crawl(url)

        return {
            "engineering": self.engineering.verify(text),
            "mba": self.mba.verify(text),
            "phd": self.phd.verify(text),
        }
