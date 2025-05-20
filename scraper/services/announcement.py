import datetime
import os

import matplotlib

matplotlib.use("Agg")

from selenium.webdriver.common.by import By

from scraper.models import Announcement

from ..utils import SeleniumDriver


class AnnouncementScraper:
    def extract_announcement(self):
        driver = None
        try:
            url = os.getenv("ANNOUNCEMENT_LINK")
            driver = SeleniumDriver.start_selenium(url)
            div_list = driver.find_elements(By.CLASS_NAME, "media")
            for div in div_list:
                date = div.find_element(By.CLASS_NAME, "text-muted").text
                date_obj = datetime.datetime.strptime(date, "%b %d, %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                link_element = div.find_element(By.TAG_NAME, "a")
                link_url = link_element.get_attribute("href")
                announcement = div.find_element(By.CLASS_NAME, "media-body").text
                if link_url:
                    driver = SeleniumDriver.start_selenium(link_url)
                    tags_list = driver.find_element(
                        By.XPATH,
                        "//*[@id='aspnetForm']/div[4]/div[5]/div/div/table/tbody/tr[5]/td[2]",
                    ).text
                    fields = [
                        field.strip()
                        for field in tags_list.split("    ")
                        if field.strip()
                    ]
                    if driver:
                        driver.quit()
                try:
                    if not Announcement.objects.filter(url=link_url).exists():
                        Announcement.objects.create(
                            date=formatted_date,
                            url=link_url,
                            announcement=announcement,
                            tags=fields,
                        )
                except Exception as e:
                    print(f"Error saving announcement: {e}")

        except Exception as e:
            print(f"Error: {e}")
            return {}
        finally:
            if driver:
                driver.quit()
