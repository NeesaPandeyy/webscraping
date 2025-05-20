import concurrent.futures
import datetime
import time

import matplotlib

matplotlib.use("Agg")

from googletrans import Translator
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from scraper.models import NewsURL, NewsURLRule, StockRecord, Symbol

from ..utils import DateConvertor, SeleniumDriver, TextTranslator


class News:
    def __init__(self):
        self.translator = Translator()

    def news(self):
        symbols = Symbol.objects.all()
        news_urls = NewsURL.objects.all()
        start = time.perf_counter()
        news_list = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            news_futures = {}

            for symbol in symbols:
                short_name = symbol.name
                full_name = symbol.full_name

                for url in news_urls:
                    future = executor.submit(self.scrape_news, full_name, url)
                    news_futures[future] = (short_name, full_name, url)

            for future in concurrent.futures.as_completed(news_futures):
                try:
                    short_name, full_name, url = news_futures[future]
                    result = future.result()

                    if isinstance(result, list) and result:
                        for item in result:
                            item["symbol"] = short_name
                            item["full_name"] = full_name
                        news_list.extend(result)
                except Exception as e:
                    print(f"General news error: {e}")

        for item in news_list:
            if not StockRecord.objects.filter(url=item["url"]).exists():
                symbol_instance = Symbol.objects.filter(name=item["symbol"]).first()
                if symbol_instance:
                    stock_record = StockRecord.objects.create(
                        symbol=symbol_instance,
                        title=item.get("title", ""),
                        url=item["url"],
                        summary=item.get("summary", ""),
                        date=item.get("date", None),
                    )
        print(news_list)

        finish = time.perf_counter()
        print(f"Finished in {round(finish - start, 2)} seconds")

    def scrape_news(self, symbol, url):
        driver = None
        try:
            rule = NewsURLRule.objects.filter(url=url).first()
            driver = SeleniumDriver.start_selenium(url.url)
            SeleniumDriver.handle_alert(driver)
            news_dict = self.search_news(driver, rule, symbol)

            results = []
            for link_url, link_text in news_dict.items():
                results.append({"symbol": symbol, "url": link_url, "title": link_text})
            return results
        except Exception as e:
            print(f"Error scraping news for symbol {symbol}: {e}")
            return {}
        finally:
            if driver:
                driver.quit()

    def search_news(self, driver, rule, symbol):
        all_news = {}
        try:
            search = driver.find_element(By.XPATH, rule.search)
            search.click()
            time.sleep(2)
            search_bar = driver.find_element(By.XPATH, rule.search_bar)
            search_bar.send_keys(symbol)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(2)
            if rule.main_div:
                main_div = driver.find_element(By.XPATH, rule.main_div)
                div_list = main_div.find_elements(By.TAG_NAME, rule.div_list)
            else:
                div_list = driver.find_elements(By.TAG_NAME, rule.div_list)
            for div in div_list:
                try:
                    link = div.find_element(By.TAG_NAME, "a")
                    link_url = link.get_attribute("href")
                    if not StockRecord.objects.filter(url=link_url).exists():
                        new_driver = SeleniumDriver.start_selenium(link)
                        content = self.detail_content(new_driver, rule)
                        all_news[link_url] = content
                except:
                    continue
        except:
            pass

        return all_news

    def detail_content(self, driver, rule):
        content = {}
        date = None
        try:
            date_orginal = driver.find_elements(By.CLASS_NAME, rule.uploaded)
            for date in date_orginal:
                date = date.text
                date = DateConvertor.date_convertor(date)

                if isinstance(date, datetime.date):
                    date = date
                    break

            headline = driver.find_element(By.TAG_NAME, rule.headline).text.replace(
                "\n", " "
            )
            if rule.summary_id:
                summary = driver.find_element(By.ID, rule.summary_id).text.replace(
                    "\n", " "
                )
            elif rule.summary_class:
                summary = driver.find_element(
                    By.CLASS_NAME, rule.summary_class
                ).text.replace("\n", " ")
            translated_title, _ = TextTranslator.translate_text(
                headline, self.translator
            )
            translated_summary, _ = TextTranslator.translate_text(
                summary, self.translator
            )
            content[translated_title] = {
                "summary": translated_summary,
                "date": date,
            }
        except Exception as e:
            print(f"Error in detail content :{e}")
        finally:
            if driver:
                driver.quit()
        return content
