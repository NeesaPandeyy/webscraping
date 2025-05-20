import os

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalysis:
    @staticmethod
    def sentiment_score_vader(sentence):
        analyze = SentimentIntensityAnalyzer()
        sentiment_dict = analyze.polarity_scores(sentence)
        return sentiment_dict["compound"]

    @staticmethod
    def sentiment_score_textblob(text):
        return TextBlob(text).sentiment.polarity

    @staticmethod
    def sentiment_label(score, method="vader"):
        if method == "vader":
            return (
                "Positive"
                if score >= 0.05
                else "Negative"
                if score <= -0.05
                else "Neutral"
            )
        else:
            return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"

    @staticmethod
    def apply_sentiment(data):
        result = data.values(
            "symbol__name", "symbol__sector__sector", "title", "summary", "date"
        )
        df = pd.DataFrame(result)
        df["sentiment_score_title_vader"] = df["title"].apply(
            SentimentAnalysis.sentiment_score_vader
        )
        df["sentiment_score_summary_vade"] = df["summary"].apply(
            SentimentAnalysis.sentiment_score_vader
        )

        df["Title_sentiment_vader"] = df["sentiment_score_title_vader"].apply(
            lambda x: SentimentAnalysis.sentiment_label(x, method="vader")
        )
        df["Summary_sentiment_vader"] = df["sentiment_score_summary_vade"].apply(
            lambda x: SentimentAnalysis.sentiment_label(x, method="vader")
        )
        df["sentiment_score_title_textblob"] = df["title"].apply(
            SentimentAnalysis.sentiment_score_textblob
        )
        df["sentiment_score_summary_textblob"] = df["summary"].apply(
            SentimentAnalysis.sentiment_score_textblob
        )

        df["Title_sentiment_textblob"] = df["sentiment_score_title_textblob"].apply(
            lambda x: SentimentAnalysis.sentiment_label(x, method="textblob")
        )
        df["Summary_sentiment_textblob"] = df["sentiment_score_summary_textblob"].apply(
            lambda x: SentimentAnalysis.sentiment_label(x, method="textblob")
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
        SentimentAnalysis.plot_chart(result_df)
        return result_json

    @staticmethod
    def plot_chart(df):
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 2, 1)
        sns.countplot(x=df["Title_sentiment_vader"], color="blue")
        plt.title("Title sentiment using vader")

        plt.subplot(2, 2, 2)
        sns.countplot(x=df["Summary_sentiment_vader"], color="green")
        plt.title("Summary Sentiment using vader")

        plt.subplot(2, 2, 3)
        sns.countplot(x=df["Title_sentiment_textblob"], color="blue")
        plt.title("Title sentiment using textblob")

        plt.subplot(2, 2, 4)
        sns.countplot(x=df["Summary_sentiment_textblob"], color="green")
        plt.title("Summary Sentiment using textblob")

        plt.tight_layout()
        output_path = os.path.join("scraper/static/scraper", "plotchart.png")
        plt.savefig(output_path)
        plt.close()
