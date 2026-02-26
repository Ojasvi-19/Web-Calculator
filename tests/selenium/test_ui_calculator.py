import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")          # REQUIRED for Jenkins
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000")
    yield driver
    driver.quit()


def test_addition(driver):
    num1 = driver.find_element(By.ID, "num1")
    num2 = driver.find_element(By.ID, "num2")
    add_btn = driver.find_element(By.ID, "add")
    result = driver.find_element(By.ID, "result")

    num1.clear()
    num2.clear()
    num1.send_keys("5")
    num2.send_keys("3")
    add_btn.click()

    time.sleep(1)
    assert result.text == "8"


def test_subtraction(driver):
    num1 = driver.find_element(By.ID, "num1")
    num2 = driver.find_element(By.ID, "num2")
    sub_btn = driver.find_element(By.ID, "subtract")
    result = driver.find_element(By.ID, "result")

    num1.clear()
    num2.clear()
    num1.send_keys("10")
    num2.send_keys("4")
    sub_btn.click()

    time.sleep(1)
    assert result.text == "6"