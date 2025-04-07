from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from langdetect import detect


def start_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    return driver


def handle_alert(driver):
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except Exception:
        pass
    try:
        close_xpaths = [
            '//button[@type="button" and @class="close" and @aria-label="Close"]',
            '//*[@id="roadblock-ad"]/div/div/i',
            '//*[@id="ratopati-app"]/div[1]/section/div/div[2]/button',
        ]
        for xpath in close_xpaths:
            try:
                close_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                close_button.click()
                break
            except (NoSuchElementException, TimeoutException):
                print("No close button")
    except (NoSuchElementException, TimeoutException):
        print("No button found")


def translate_text(line, translator):
    if line.strip():
        try:
            detected_lang = detect(line)
            translated_en = (
                translator.translate(line, dest="en").text
                if detected_lang != "en"
                else line
            )
            translated_ne = (
                translator.translate(line, dest="ne").text
                if detected_lang != "ne"
                else line
            )
            return translated_en, translated_ne
        except Exception as e:
            print(f"Error: {e}")
    return line, line


def regex_search_button(driver, name, rule):
    regex = re.compile(r".*(Company name or symbol).*|.*search.*", re.IGNORECASE)

    try:
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        for input_field in input_fields:
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of(input_field))
                placeholder = input_field.get_attribute("placeholder")
                if not placeholder or regex.match(placeholder):
                    input_field.send_keys(name)
                    input_field.send_keys(Keys.RETURN)
                    if rule.click_button:
                        a = driver.find_element(By.XPATH, rule.click_button)
                        a.click()
                        handle_alert(driver)
            except Exception as e:
                print(f"Error:{e}")
    except Exception as e:
        print(f"Error: {e}")


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
        print(f"Error: {e}")


def dropdown_control(driver):
    try:
        dropdown_element = driver.find_element(
            By.XPATH,
            '//select[contains(@name, "length") or contains(@name, "Limit")]',
        )
        dropdown = Select(dropdown_element)
        dropdown.select_by_value("50")
    except Exception as e:
        print(f"Error Message: {e}")
        print("No dropdown1")

    time.sleep(1)
    driver.implicitly_wait(2)

    try:
        dropdown_element = driver.find_element(
            By.XPATH,
            '//select[contains(@name, "Limit") or contains(@name, "length")]',
        )
        dropdown = Select(dropdown_element)
        dropdown.select_by_value("50")
    except:
        print("No dropdown2")

    time.sleep(2)
