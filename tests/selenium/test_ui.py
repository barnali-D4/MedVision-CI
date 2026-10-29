
import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def browser():
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-mode")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    driver = webdriver.Edge(options=options)
    yield driver
    driver.quit()


def test_homepage_opens_in_browser(browser):
    browser.get("http://127.0.0.1:5000/")

    assert browser.title == "MedVision-CI | Chest X-Ray Analysis"
    assert "MedVision-CI" in browser.find_element(
        By.TAG_NAME, "h1"
    ).text
    assert "Analyze Image" in browser.page_source


def test_valid_image_upload(browser, tmp_path):
    browser.get("http://127.0.0.1:5000/")

    image_path = tmp_path / "test.png"
    Image.new("RGB", (64, 64), color="white").save(image_path)

    browser.find_element(By.ID, "image").send_keys(str(image_path))
    browser.find_element(
        By.CSS_SELECTOR, "#upload-form button[type='submit']"
    ).click()

    result = WebDriverWait(browser, 30).until(
        lambda driver: (
            text
            if (
                (text := driver.find_element(By.ID, "result").text)
                and "Image classified successfully." in text
            )
            else False
        )
    )

    assert "Prediction:" in result
    assert "Confidence:" in result
    assert "Class probabilities:" in result
    assert "NORMAL" in result
    assert "PNEUMONIA" in result
