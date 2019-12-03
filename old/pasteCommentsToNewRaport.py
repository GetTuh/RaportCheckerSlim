from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import importlib
waitForLoadToFinish = importlib.import_module("waitForLoadingToFinish")


def WFLTF(driver):
    waitForLoadToFinish.waitForLoadToFinish(driver)


def pasteCommentsToNewRaport(driver, newlist, NewRepLink):
    try:
        driver.get(NewRepLink)
        time.sleep(1)
        extend = driver.find_element_by_class_name("k-pager-wrap")
        extend.find_element_by_class_name("k-select").click()
        WFLTF(driver)
        driver.find_element_by_xpath(
            "//li[contains(@class, 'k-item')][7]").click()
    except:
        driver.quit()
        driver = webdriver.Chrome(
            "C:\Program Files (x86)\Google\chromedriver.exe")
        pasteCommentsToNewRaport(driver, newlist, NewRepLink)
    WFLTF(driver)

    def addComment(item, count):
        WFLTF(driver)
        try:
            new_Comment = driver.find_element_by_xpath(
                '//*[@id="SummaryResultResultsTableRouteGridName"]/div[4]/table/tbody/tr[' + str(count) + ']/td[4]')
            # if new_Comment!="add" or :

            new_Comment.click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '//*[@id="resultComment"]').send_keys(item[1])
            driver.find_element_by_xpath(
                '//*[@id="saveTextInputButton"]').click()
            WFLTF(driver)
        except:
            print(item[0] + " already has a comment")

    howManyTests = len(driver.find_elements_by_xpath(
        "//*[@id=\"SummaryResultResultsTableRouteGridName\"]/div[4]/table/tbody/tr")) + 1
    for x in range(1, howManyTests):
        print(x)
        for z in newlist:
            # time.sleep(1)
            print(driver.find_element_by_xpath(
                "//*[@id=\"SummaryResultResultsTableRouteGridName\"]/div[4]/table/tbody/tr[" + str(x) + "]/td[2]").text)
            if z[0] == driver.find_element_by_xpath("//*[@id=\"SummaryResultResultsTableRouteGridName\"]/div[4]/table/tbody/tr[" + str(x) + "]/td[2]").text:
                addComment(z, x)
