from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")

                #An Empty Text file that can save the results that we gained when we run.
                textFile = open("reports.txt", "w")

                #Adds all the results to the text file, used in the report later.

                #Answers #1 -> Print number of unique pages
                print("# of unique pages: " + str(len(scraper.global_linkNumWords_dictionary)))
                textFile.write("# of unique pages: " + str(len(scraper.global_linkNumWords_dictionary)) + "\n")

                #Answers #2 -> Longest page in terms of num of words
                #Sorts the dictionary based on the largest value (aka # of words), and we grab the first item (highest value)
                longestPage = sorted(scraper.global_linkNumWords_dictionary.items(), key = lambda item: (-item[1]))[0][0]
                print("Page with longest number of words: "  + longestPage + "\n")
                textFile.write("Page with longest number of words: "  + str(longestPage) + "\n")

                #Answers #3 -> 50 most common words in the links
                #Sorts based on the freq of the word (how many times its there)
                firstFiftyWords = sorted(scraper.global_words_dictionary.items(), key = lambda item: (-item[1]))[:50]
                for eachWord in firstFiftyWords:
                    print("Word: " + eachWord[0] + "    Count: " + str(eachWord[1]))
                    textFile.write("Word: " + eachWord[0] + "    Count: " + str(eachWord[1]) + "\n")

                #Answers #4 -> Unique ics subdomains, listed alphabetically
                #Sorts them alphabetically based on the link
                icsSubdomains = sorted(scraper.global_icsLink_dictionary.items(), key = lambda item: (item[0]))
                for eachLink in icsSubdomains:
                    textFile.write("Link: " + eachLink[0] + "    Count: " + str(eachLink[1]) + "\n")

                #Closes the file
                textFile.close()

                #Ends the run
                break
            if tbd_url not in scraper.global_linkNumWords_dictionary:
                resp = download(tbd_url, self.config, self.logger)
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")
                scraped_urls = scraper.scraper(tbd_url, resp)
                for scraped_url in scraped_urls:
                    self.frontier.add_url(scraped_url)
                self.frontier.mark_url_complete(tbd_url)
                time.sleep(self.config.time_delay)
