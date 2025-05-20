import datetime
import re
import time

import nepali_datetime
from langdetect import detect
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumDriver:
    @staticmethod
    def start_selenium(url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(2)
        return driver

    @staticmethod
    def handle_alert(driver):
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except Exception:
            print(f"Error in handling alert:{Exception}")
        try:
            close_xpaths = [
                '//button[@type="button" and @class="close" and @aria-label="Close"]',
                '//*[@id="roadblock-ad"]/div/div/i',
                '//*[@id="ratopati-app"]/div[1]/section/div/div[2]/button',
                '//*[@id="onesignal-slidedown-cancel-button"]',
            ]
            for xpath in close_xpaths:
                try:
                    close_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    close_button.click()
                    break
                except (NoSuchElementException, TimeoutException):
                    print("No close button")
        except (NoSuchElementException, TimeoutException):
            print("No button found")


class TextTranslator:
    @staticmethod
    def translate_text(line, translator):
        if line and line.strip():
            try:
                detected_lang = detect(line)

                translated_en = line
                translated_ne = line

                if detected_lang != "en":
                    translated_result = translator.translate(line, dest="en")
                    if translated_result and hasattr(translated_result, "text"):
                        translated_en = translated_result.text

                if detected_lang != "ne":
                    translated_result = translator.translate(line, dest="ne")
                    if translated_result and hasattr(translated_result, "text"):
                        translated_ne = translated_result.text

                return translated_en, translated_ne

            except Exception as e:
                print(f"Error in translating text: {e}")

        return line, line


class NewsScraping:
    @staticmethod
    def regex_search_button(driver, name, rule):
        regex = re.compile(r".*(Company name or symbol).*|.*search.*", re.IGNORECASE)

        try:
            input_fields = driver.find_elements(By.TAG_NAME, "input")
            for input_field in input_fields:
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of(input_field))
                    placeholder = input_field.get_attribute("placeholder")
                    if not placeholder or regex.match(placeholder):
                        input_field.send_keys(name)
                        input_field.send_keys(Keys.RETURN)
                        try:
                            if rule.click_button:
                                a = driver.find_element(By.XPATH, rule.click_button)
                                a.click()
                                SeleniumDriver.handle_alert(driver)
                        except Exception as e:
                            print(f"Error in regrex1:{e}")
                except Exception as e:
                    print(f"Error in regrex2:{e}")
        except Exception as e:
            print(f"Error in regrex1: {e}")

    @staticmethod
    def news_block(driver):
        try:
            ul_element = driver.find_element(By.CSS_SELECTOR, "ul.nav")
            li_elements = ul_element.find_elements(By.TAG_NAME, "li")
            for li in li_elements:
                if "news" in li.text.lower():
                    a_element = li.find_element(By.TAG_NAME, "a")
                    driver.execute_script("arguments[0].click();", a_element)
                    break
        except Exception as e:
            print(f"Error in news block: {e}")

    def dropdown_control(driver):
        try:
            dropdown_element = driver.find_element(
                By.XPATH,
                '//select[contains(@name, "length") or contains(@name, "Limit")]',
            )
            dropdown = Select(dropdown_element)
            dropdown.select_by_value("50")
        except Exception as e:
            print(f"Error in dropdown control: {e}")
            print("No dropdown1")

        time.sleep(5)
        driver.implicitly_wait(10)

        try:
            dropdown_element = driver.find_element(
                By.XPATH,
                '//select[contains(@name, "Limit") or contains(@name, "length")]',
            )
            dropdown = Select(dropdown_element)
            dropdown.select_by_value("50")
        except Exception as e:
            print(f"Error in dropdown control: {e}")
            print("No dropdown2")

        time.sleep(1)


class DateConvertor:
    @staticmethod
    def date_convertor(date_org):
        nepali_to_english_digit = str.maketrans("०१२३४५६७८९", "0123456789")

        nepali_months = {
            "वैशाख": 1,
            "जेठ": 2,
            "असार": 3,
            "साउन": 4,
            "भदौ": 5,
            "असोज": 6,
            "कात्तिक": 7,
            "मंसिर": 8,
            "पुस": 9,
            "पुष": 9,
            "माघ": 10,
            "फागुन": 11,
            "चैत": 12,
        }
        english_months = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }

        date_org = date_org.translate(nepali_to_english_digit)

        match = re.search(r"(\d+)\s+([^\s]+)\s+(\d+)\s+गते", date_org)

        if match:
            try:
                year = int(match.group(1))
                month_nep = match.group(2)
                day = int(match.group(3))

                month = nepali_months.get(month_nep)
                if not month:
                    return None

                nepali_dt = nepali_datetime.date(year, month, day)
                return nepali_dt.to_datetime_date()
            except Exception as e:
                print("Nepali date error:", e)
                return None

        match = re.search(r"([A-Za-z]{3}) (\d{1,2}), (\d{4})", date_org)
        if match:
            try:
                month_eng = match.group(1)
                day = int(match.group(2))
                year = int(match.group(3))

                month = english_months.get(month_eng)
                if not month:
                    return None

                return datetime.date(year, month, day)
            except Exception as e:
                print("English date error:", e)
                return None

        return None
