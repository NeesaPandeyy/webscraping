import concurrent.futures
import datetime
import re
import time

import matplotlib

matplotlib.use("Agg")

from googletrans import Translator
from selenium.webdriver.common.by import By

from scraper.models import StockNewsURL, StockNewsURLRule, StockRecord, Symbol

from ..utils import DateConvertor, NewsScraping, SeleniumDriver, TextTranslator


class StockNews:
    def __init__(self):
        self.translator = Translator()

    def stock_news(self):
        symbols = Symbol.objects.all()
        stock_urls = StockNewsURL.objects.all()
        start = time.perf_counter()
        stock_list = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            stock_futures = {}

            for symbol in symbols:
                short_name = symbol.name
                full_name = symbol.full_name

                for url in stock_urls:
                    future = executor.submit(
                        self.single_keyword_scrape, short_name, url
                    )
                    stock_futures[future] = (short_name, full_name, url)

            for future in concurrent.futures.as_completed(stock_futures):
                try:
                    short_name, full_name, url = stock_futures[future]
                    result = future.result()

                    if isinstance(result, list) and result:
                        for item in result:
                            item["symbol"] = short_name
                            item["full_name"] = full_name
                        stock_list.extend(result)
                except Exception as e:
                    print(f"Stock news error: {e}")
        for item in stock_list:
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

        finish = time.perf_counter()
        print(f"Finished in {round(finish - start, 2)} seconds")

    def single_keyword_scrape(self, key_word, url):
        driver = None
        try:
            rule = StockNewsURLRule.objects.filter(url=url).first()
            driver = SeleniumDriver.start_selenium(url.url)
            SeleniumDriver.handle_alert(driver)
            NewsScraping.regex_search_button(driver, key_word, rule)

            try:
                NewsScraping.news_block(driver)
            except Exception as e:
                print(f"Error in news_block: {e}")

            try:
                NewsScraping.dropdown_control(driver)
            except Exception as e:
                print(f"No dropdown: {e}")

            news_dict = self.news_extraction(driver, rule)

            results = []
            for link_url, link_detail in news_dict.items():
                for title, detail in link_detail.items():
                    results.append(
                        {
                            "symbol": key_word,
                            "url": link_url,
                            "title": title,
                            "summary": detail["summary"],
                            "date": detail["date"],
                        }
                    )
            return results
        except Exception as e:
            print(f"Error in single_keyword_scrape {url.url} for {key_word}: {e}")
            return {}
        finally:
            if driver:
                driver.quit()

    def news_extraction(self, driver, rule):
        all_news = {}
        try:
            if rule.main_div:
                regex_class = re.compile(r".*news.*", re.IGNORECASE)
                main_div = driver.find_elements(By.TAG_NAME, rule.main_div)
                for div in main_div:
                    div_class = div.get_attribute("id")
                    if regex_class.search(div_class):
                        tbody = div.find_element(By.TAG_NAME, rule.tbody)
                        rows = tbody.find_elements(By.TAG_NAME, rule.rows)
                        for row in rows:
                            link_element = row.find_element(By.TAG_NAME, "a")
                            link_url = link_element.get_attribute("href")
                            if not StockRecord.objects.filter(url=link_url).exists():
                                new_driver = SeleniumDriver.start_selenium(link_url)
                                time.sleep(5)
                                content = self.detail_content(new_driver, rule)
                                all_news[link_url] = content
            else:
                div_list = driver.find_element(By.XPATH, rule.div_list)
                rows = div_list.find_elements(By.TAG_NAME, "a")
                for row in rows:
                    link_url = row.get_attribute("href")
                    if not StockRecord.objects.filter(url=link_url).exists():
                        new_driver = SeleniumDriver.start_selenium(link_url)
                        time.sleep(5)
                        content = self.detail_content(new_driver, rule)
                        all_news[link_url] = content
        except Exception as e:
            print(f"Error in news_extraction: {e}")
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
