## Django Stock News Sentiment Analysis

A Django-based stock news platform that automatically scrapes news articles from configurable URLs, performs sentiment analysis, and shows results via a REST API. The project uses **Selenium** for scraping, **Celery** for daily task scheduling, and **TextBlob + VADER** for sentiment analysis. It features a clean admin panel for managing sources and supports filtering results by symbol, sector, and date.

---

## Features

- **Django Admin**: Configure stock news source URLs easily.
- **Automated Scraping**: Uses Selenium to scrape stock news daily.
- **Celery Scheduler**: Scheduled scraping tasks using Celery with Redis.
- **Sentiment Analysis**: Implements TextBlob and VADER for sentiment scoring.
- **REST API**: Django REST Framework-powered API to fetch and filter stock sentiment data.
- **Filtering**: Filter news and sentiment data by stock symbol, sector, or date.
- **PostgreSQL**: Database backend.

---

## Technology Used

- Django
- Django REST Framework
- Selenium
- Celery
- TextBlob
- VADER
- PostgreSQL
- Redis (for Celery Broker)