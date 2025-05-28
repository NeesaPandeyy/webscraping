# Django Stock News Sentiment Analysis

A Django-based stock news platform that automatically scrapes news articles from configurable URLs, performs sentiment analysis, and exposes results via a REST API. The project uses **Selenium** for scraping, **Celery** for task scheduling, and **TextBlob + VADER** for sentiment analysis. It includes Google OAuth login, email notifications, custom news posting, and a threaded comment system with likes. Admins can manage content via a modern UI built with Django Unfold.

---

## Features

- **Django Admin**: Configure stock news source URLs easily.
- **Automated Scraping**: Uses Selenium to scrape stock news daily.
- **Custom News Posts**: Create and manage custom news via a dedicated model and API.
- **User Authentication**: Supports Google OAuth2 login.
- **Email Notifications**: Sends email alerts on registration and when new posts are added.
- **Comment System**: Nested (tree-structured) comments for each post.
- **Like Feature**: Users can like posts.
- **Celery Scheduler**: Scheduled scraping tasks using Celery with Redis.
- **Sentiment Analysis**: Implements TextBlob and VADER for sentiment scoring.
- **REST API**: Django REST Framework-powered API to fetch and filter stock sentiment data.
- **Filtering**: Filter news and sentiment data by stock symbol, sector, or date.
- **Modern Admin UI**: Enhanced with Django Unfold theme.
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
- Redis (for Celery broker)
- Django Unfold
- Google OAuth2
