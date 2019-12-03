from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import importlib

waitForLoadToFinish = importlib.import_module("waitForLoadingToFinish")


def WFLTF(driver):
    waitForLoadToFinish.waitForLoadToFinish(driver)


def deleteComments(link):
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
    driver.get(link)
    time.sleep(2)

    driver.find_element_by_xpath(
        '//*[@id="SummaryResultResultsTableRouteGridName"]/div[5]/span[1]/span/span').click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[contains(@class, 'k-item')][7]").click()
    time.sleep(2)
    driver.find_elements_by_class_name('k-header-column-menu')[6].click()
    time.sleep(.2)
    driver.find_element_by_class_name('k-i-sort-desc-sm').click()
    WFLTF(driver)
    time.sleep(1)
    while True:
        try:
            elem = driver.find_element_by_xpath(
                '//*[@id="SummaryResultResultsTableRouteGridName"]/div[4]/table/tbody/tr[1]/td[4]/span')
        except:
            break
        if (elem.text != 'add'):
            elem.click()
            driver.find_element_by_xpath('//*[@id="resultComment"]').clear()
            driver.find_element_by_xpath(
                '//*[@id="saveTextInputButton"]').click()
            WFLTF(driver)
            time.sleep(.1)
        else:
            break
    print("Done")
