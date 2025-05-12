import time
from os import scandir
from traceback import print_tb

import bs4
import aiohttp
import asyncio
import feedparser

class ScraperUrl:
    def __init__(self):
        self.soup_class = bs4.BeautifulSoup(features="html.parser")

    @staticmethod
    async def process_url(url)->list[str]:
        html = await scraper.fetch(url)
        return html

    @staticmethod
    def load_url(filename:str)->list[str]|str:
        try :
            with open(filename, "r") as f:
                return [
                    url.strip() for url in f.readlines() if url.strip().lower().startswith("http://") or url.strip().lower().startswith("https://")
                ]
        except FileNotFoundError as e:
            return f"Error : {e}"

    @staticmethod
    async def fetch(url: str) -> list:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content_type = response.headers.get('Content-Type', '').lower()
                    charset = None
                    if 'charset=' in content_type:
                        #On récupère le charset du flux rss pour décoder le flux
                        charset = content_type.split('charset=')[-1].split(';')[0].strip()
                    try:
                        #on tente de décoder le xml avec l'encodage du flux
                        xml = await response.text(encoding=charset) if charset else await response.text()
                    except UnicodeDecodeError:
                        #si le décodage est mal executé on tente en utf-8
                        xml = (await response.read()).decode('utf-8', errors='replace')
                    feed = feedparser.parse(xml)
                    articles = []
                    for entry in feed.entries:
                        articles.append({
                            "title": entry.get("title", "N/A"),
                            "link": entry.get("link", "N/A"),
                            "summary": entry.get("summary", ""),
                            "published": entry.get("published", "N/A")
                        })
                    return articles
        except Exception as e:
            print(f"[!] Erreur sur {url} : {e}")
            return []

class Searcher:
    def __init__(self, keyword:str,keyword_2:str = None,keyword_3:str = None,):
        self.keyword = keyword
        self.keyword2 = keyword_2
        self.keyword3 = keyword_3

    @staticmethod
    def keyword_evaluator(keyword:str, article:dict)->bool:
        return keyword in article["title"].lower() or keyword in article["summary"].lower()

    async def search_in_article(self, article:dict):
        best_search = []
        second_best = []
        third_best = []
        count = 0
        keywords_matched = []

        for kw in [self.keyword, self.keyword2, self.keyword3]:
            if kw is None:
                continue
            if self.keyword_evaluator(kw, article):
                count += 1
                keywords_matched.append(kw)
        if count == 1 :
            third_best.append(f"title : {article['title']}, link : {article['link']}, published : {article['published']}, keyword : {keywords_matched}")
        if 1 < count < 3:
            second_best.append(f"title : {article['title']},link : {article['link']}, published : {article['published']},keyword : {keywords_matched}")
        if count == 3:
            best_search.append(f"title : {article['title']},link : {article['link']}, published : {article['published']},keyword : {keywords_matched}")
        return best_search, second_best, third_best

async def main():
    tasks = [scraper.process_url(url) for url in list_urls]
    results: list = await asyncio.gather(*tasks)
    return results

async def search(parsed:list[dict])->list:
    tasks = [searcher.search_in_article(text) for text in parsed]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    scraper = ScraperUrl()
    searcher = Searcher("nutella")
    start = time.time()
    list_urls = scraper.load_url("rss_list.txt")
    results_parsing = asyncio.run(main())

    with open("resultats.txt", "w", encoding="utf-16") as f:
        best = []
        second = []
        least = []
        results_search = asyncio.run(search(results_parsing[0]))
        if results_search:
            for evaluation in results_search:
                best.append(evaluation[0])
                second.append(evaluation[1])
                least.append(evaluation[2])
        for value in best:
            if value:
                f.write(f"{value[0]}\n")
        for value in second:
            if value:
                f.write(f"{value[0]}\n")
        for value in least:
            if value:
                f.write(f"{value[0]}\n")
    end = time.time()
    print(f"execution time : {end - start} seconds")

    print("Résultats enregistrés dans resultats.txt")
