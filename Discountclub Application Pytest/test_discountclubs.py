import time

import pytest
import pytest_html
import allure_pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from allure import severity, severity_level
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Fixture for Chrome or Firefox -- We can use this to initiate and close the driver(Browser)
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    # yield
    # chrome_driver.close()


# @allure.severity(allure.severity_level.NORMAL)
# class TestDiscountClub:
# @allure.severity(allure.severity_level.MINOR)
class Test_DiscountClub():
    def test_launchsetup(self):
        global driver
        # driver = webdriver.Chrome(executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        # driver.set_page_load_timeout(0.8)
        driver.implicitly_wait(4)
        # to open the url in browser
        driver.get("https://www.discountclubs.com/home")
        parent_window = driver.current_window_handle
        print(parent_window)


@allure.severity(allure.severity_level.MINOR)
def test_login():
    email_ent = driver.find_element("id", "Email")
    email_ent.send_keys("backlinkscorner@gmail.com")
    password_ent = driver.find_element("id", "Password")
    password_ent.send_keys("Creo@123")
    log_in = driver.find_element("id", "loginButton")
    log_in.click()


@allure.severity(allure.severity_level.CRITICAL)
def test_getwelcometext():
    verify_welcometext = driver.find_element("xpath", "//h1[text()='Welcome to Discount Clubs! ']").text
    print("The welcome text is: " + verify_welcometext)
    # Used Assertion to verify the Text which is Equal or Not!!
    assert "Welcome to Discount Clubs!" in verify_welcometext, "Both are not Equal"
    print("Both are Equal")


def test_getoffertext_signout():
    parent_window = driver.current_window_handle
    gymboree_btn = driver.find_element("xpath", "(//a[@href='/goods-and-services/gymboree/'])[2]")
    gymboree_btn.click()
    get_offer = driver.find_element("xpath", "//a[contains(@class,'btn btn-primary')]")
    get_offer.click()
    all_handles = driver.window_handles
    print(all_handles)
    for handle in all_handles:
        if handle != parent_window:
            driver.switch_to.window(handle)
    verify_pagetitle = driver.title
    print(verify_pagetitle)
    # Used Assert to verify the Title which is Equal or Not!!
    try:
        assert "Kids, Toddler & Baby Clothes | Gymboree" in verify_pagetitle
        print("Validation Passed")
    except Exception as e:
        print("Validation Failed", format(e))
    try:
        popup_close = driver.find_element("xpath", "//*[@id='bx-close-inside-1732696']/svg")
        popup_close.click()
        print("pop up window successfully closed")
    except Exception:
        print("popup window not showing")
    # Used Assert to verify the Offer Text which is Equal or Not!!
    try:
        offerbanner_text = driver.find_element("xpath", "//span[contains(@class,'sc-c703a57-0 gZRUjm')]").text
        # print("The Verify Banner offer Text is: " + offerbanner_text)
        assert "UP TO 60% OFF EVERYTHING!" in offerbanner_text
        print("Assert Test Passed")
    except Exception:
        print("Assert Test Failed")
        # driver.close()
    # def test_signout(parent_window=None):
    time.sleep(5)
    driver.switch_to.window(parent_window)
    time.sleep(5)
    side_bar = driver.find_element("xpath", "//i[@class='fas fa-bars']")
    side_bar.click()
    time.sleep(5)
    sign_out = driver.find_element("id", "logoutLink")
    sign_out.click()
    print("The parent window title is: " + driver.title)


@allure.severity(allure.severity_level.NORMAL)
def test_teardown():
    # driver.close()
    driver.quit()
    print("Test Completed")
