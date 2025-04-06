from .utils import (
    start_selenium,
    handle_alert,
    regex_search_button,
    news_block,
    dropdown_control,
    translate_text
)
from dashboard.models import (
    StockNewsURL,
    StockNewsURLRule,
    NewsURL,
    NewsURLRule,
    StockRecord,
    Symbol
)
from celery import shared_task
import time
import concurrent.futures
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import json
from langdetect import detect
from googletrans import Translator

import logging


@shared_task(name="scheduling")
def stock_news():
    symbols = Symbol.objects.all() 
    news_urls = NewsURL.objects.all()
    stock_urls = StockNewsURL.objects.all()
    start = time.perf_counter()
    news_list = []
    stock_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        stock_futures = {}  
        news_futures = {}   

        for symbol in symbols:
            short_name = symbol.name
            full_name = symbol.full_name  

            for url in stock_urls:
                future = executor.submit(single_keyword_scrape, short_name, url)
                stock_futures[future] = (short_name, full_name, url)

        for symbol in symbols:
            short_name = symbol.name
            full_name = symbol.full_name  

            for url in news_urls:
                future = executor.submit(scrape_news, full_name, url)  
                news_futures[future] = (short_name, full_name, url)

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

    all_items = stock_list + news_list
    for item in all_items:
        if not StockRecord.objects.filter(url=item["url"]).exists():  
            symbols = Symbol.objects.filter(name=item["symbol"])  
            stock_record = StockRecord.objects.create(
                title=item["title"], 
                url=item["url"]
            )
            stock_record.symbol.set(symbols)  
            if "full_name" in item:
                stock_record.full_name = item["full_name"]
            stock_record.save()

    finish = time.perf_counter()
    print(f"Finished in {round(finish - start, 2)} seconds")
    
def scrape_news(symbol, url):
    driver = None
    try:
        rule = NewsURLRule.objects.filter(url=url).first()
        driver = start_selenium(url.url)
        handle_alert(driver)
        news_dict = search_news(driver, rule, symbol)
        
        results = []
        for link_url, link_text in news_dict.items():
            results.append({
                'symbol': symbol,
                'url': link_url,
                'title': link_text
            })        
        return results
    except Exception as e:
        print(f"Error scraping news for symbol {symbol}: {e}")
        return {} 
    finally:
        if driver:
            driver.quit()


def search_news(driver, rule,symbol):
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
                if rule.link_text:
                    link_text = div.find_element(By.CLASS_NAME, rule.link_text).text
                else:
                    link_text = link.text
                all_news[link_url] = link_text
            except:
                continue
    except:
        pass
    
    return all_news


def news_extraction(driver, rule):
    all_news = dict()
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
                        if rule.p_element:
                            p_element = link_element.find_element(By.TAG_NAME, "p")
                            link_text = p_element.text
                        else:
                            link_text = link_element.text
                        all_news[link_url] = link_text
        else:
            div_list = driver.find_element(By.XPATH,rule.div_list)
            rows = div_list.find_elements(By.TAG_NAME, "a")
            for row in rows:
                link_url = row.get_attribute("href")
                p_element = row.find_element(By.TAG_NAME, "p")
                link_text = p_element.text
                all_news[link_url] = link_text
    except Exception as e:
        print(f"Error in news_extraction: {e}")
    return all_news

def single_keyword_scrape(key_word, url):
    driver = None
    try:
        rule = StockNewsURLRule.objects.filter(url=url).first()
        driver = start_selenium(url.url)
        handle_alert(driver)
        regex_search_button(driver, key_word,rule)

        try:
            news_block(driver)
        except Exception as e:
            print(f"Error in news_block: {e}")
        
        try:
            dropdown_control(driver)
        except Exception as e:
            print(f"No dropdown: {e}")
        
        news_dict = news_extraction(driver, rule)
       
        results = []
        for link_url, link_text in news_dict.items():
            results.append({
                'symbol': key_word,
                'url': link_url,
                'title': link_text
            })        
        return results
    except Exception as e:
        print(f"Error in {url.url} for {key_word}: {e}")
        return {}  
    finally:
        if driver:
            driver.quit()

def keyword_data(symbol, keyword_list):
    data = StockRecord.objects.filter(symbol=symbol)
    symbol_data = [(record.title ,record.url) for record in data]
    print(symbol_data)
    translator = Translator()
    translated_keywords = {}  
    for keyword in keyword_list:
        translated_en, translated_ne = translate_text(keyword, translator)
        translated_keywords[translated_en] = translated_ne


# def keyword_data(symbol, keyword_list):
#     data = StockRecord.objects.filter(symbol=symbol)
#     title_list = [record.title for record in data]
#     url_list = [record.url for record in data]
#     translator = Translator()
#     translated_keywords = {}  
#     for keyword in keyword_list:
#         translated_en, translated_ne = translate_text(keyword, translator)
#         translated_keywords[translated_en] = translated_ne

#     for title in title_list:
#         for org_keyword,trans_keyword in translated_keywords.items():
#             if org_keyword in title or trans_keyword in title:
#                 translated_title = translate_text(title, translator)
#                 title = translated_title[0]
#                 print(title)
                

