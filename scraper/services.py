import concurrent.futures
import datetime
import re
import time
import os

import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import seaborn as sns
from celery import shared_task
from googletrans import Translator
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from dashboard.models import (NewsURL, NewsURLRule, StockNewsURL,
                              StockNewsURLRule, StockRecord, Symbol)

from .utils import (date_convertor, dropdown_control, handle_alert, news_block,
                    regex_search_button, start_selenium, translate_text)


@shared_task(name="scheduling")
def stock_news():
    symbols = Symbol.objects.all()
    news_urls = NewsURL.objects.all()
    stock_urls = StockNewsURL.objects.all()
    start = time.perf_counter()
    stock_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        stock_futures = {}
        news_futures = {}

        for symbol in symbols:
            short_name = symbol.name
            full_name = symbol.full_name

            for url in stock_urls:
                future = executor.submit(single_keyword_scrape, short_name, url)
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


def scrape_news(symbol, url):
    driver = None
    try:
        rule = NewsURLRule.objects.filter(url=url).first()
        driver = start_selenium(url.url)
        handle_alert(driver)
        news_dict = search_news(driver, rule, symbol)

        results = []
        for link_url, link_text in news_dict.items():
            results.append({"symbol": symbol, "url": link_url, "title": link_text})
        return results
    except Exception as e:
        print(f"Error in scrape news for symbol {symbol}: {e}")
        return {}
    finally:
        if driver:
            driver.quit()


def search_news(driver, rule, symbol):
    all_news = dict()
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
                new_driver = start_selenium(link_url)
                time.sleep(2)
                content = detail_content(new_driver, rule)
                all_news[link_url] = content
            except:
                continue
    except Exception as e:
        print(f"Error in search news block:{e}")

    return all_news


def news_extraction(driver, rule):
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
                            new_driver = start_selenium(link_url)
                            content = detail_content(new_driver, rule)
                            all_news[link_url] = content
        else:
            div_list = driver.find_element(By.XPATH, rule.div_list)
            rows = div_list.find_elements(By.TAG_NAME, "a")
            for row in rows:
                link_url = row.get_attribute("href")
                if not StockRecord.objects.filter(url=link_url).exists():
                    new_driver = start_selenium(link_url)
                    time.sleep(2)
                    content = detail_content(new_driver, rule)
                    all_news[link_url] = content
    except Exception as e:
        print(f"Error in news_extraction: {e}")
    return all_news


def single_keyword_scrape(key_word, url):
    driver = None
    try:
        rule = StockNewsURLRule.objects.filter(url=url).first()
        driver = start_selenium(url.url)
        handle_alert(driver)
        regex_search_button(driver, key_word, rule)

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


def detail_content(driver, rule):
    translator = Translator()
    content = {}
    date = None
    try:
        date_orginal = driver.find_elements(By.CLASS_NAME, rule.uploaded)
        for date in date_orginal:
            date = date.text
            date = date_convertor(date)

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
        translated_title, _ = translate_text(headline, translator)
        translated_summary, _ = translate_text(summary, translator)
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


def sentiment_score_vader(sentence):
    analyze = SentimentIntensityAnalyzer()
    sentiment_dict = analyze.polarity_scores(sentence)
    return sentiment_dict["compound"]


def sentiment_score_textblob(text):
    return TextBlob(text).sentiment.polarity


def sentiment_label(score, method="vader"):
    if method == "vader":
        return (
            "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"
        )
    else:
        return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"


def apply_sentiment(data):
    result = data.values(
        "symbol__name", "symbol__sector__sector", "title", "summary", "date"
    )
    df = pd.DataFrame(result)
    df["sentiment_score_title_vader"] = df["title"].apply(sentiment_score_vader)
    df["sentiment_score_summary_vade"] = df["summary"].apply(sentiment_score_vader)

    df["Title_sentiment_vader"] = df["sentiment_score_title_vader"].apply(
        lambda x: sentiment_label(x, method="vader")
    )
    df["Summary_sentiment_vader"] = df["sentiment_score_summary_vade"].apply(
        lambda x: sentiment_label(x, method="vader")
    )
    df["sentiment_score_title_textblob"] = df["title"].apply(sentiment_score_textblob)
    df["sentiment_score_summary_textblob"] = df["summary"].apply(
        sentiment_score_textblob
    )

    df["Title_sentiment_textblob"] = df["sentiment_score_title_textblob"].apply(
        lambda x: sentiment_label(x, method="textblob")
    )
    df["Summary_sentiment_textblob"] = df["sentiment_score_summary_textblob"].apply(
        lambda x: sentiment_label(x, method="textblob")
    )
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["symbol_name"] = df["symbol__name"]
    df["sector"] = df["symbol__sector__sector"]

    result_df = df[
        [
            "symbol_name",
            "sector",
            "date",
            "title",
            "summary",
            "Title_sentiment_vader",
            "Summary_sentiment_vader",
            "Title_sentiment_textblob",
            "Summary_sentiment_textblob",
        ]
    ]
    result_json = result_df.to_json(orient="records", force_ascii=False)
    plot_chart(result_df)
    return result_json

def plot_chart(df):
    plt.figure(figsize=(12,6))

    plt.subplot(2,2,1)
    sns.countplot(x=df['Title_sentiment_vader'],color="blue")
    plt.title("Title sentiment using vader")

    plt.subplot(2, 2, 2)
    sns.countplot(x=df["Summary_sentiment_vader"], color="green")
    plt.title("Summary Sentiment using vader")

    plt.subplot(2,2,3)
    sns.countplot(x=df['Title_sentiment_textblob'],color="blue")
    plt.title("Title sentiment using textblob")

    plt.subplot(2, 2, 4)
    sns.countplot(x=df["Summary_sentiment_textblob"], color="green")
    plt.title("Summary Sentiment using textblob")
    
    plt.tight_layout()
    output_path = os.path.join("dashboard/static/dashboard", "plotchart.png")
    plt.savefig(output_path)
    plt.close()

