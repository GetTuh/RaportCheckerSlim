import importlib
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import itertools
scrapeBasicInfo = importlib.import_module("scrapeBasicInfo")
waitForLoadToFinish = importlib.import_module("waitForLoadingToFinish")


def WFLTF(driver):
    waitForLoadToFinish.waitForLoadToFinish(driver)


def get_html(driver, link):
    try:
        driver.get(link)
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="SummaryResultResultsTableRouteGridName"]/div[5]/span[1]/span/span').click()
        time.sleep(.4)
        driver.find_element_by_xpath(
            "//li[contains(@class, 'k-item')][7]").click()
    except:
        get_html(driver, link)
    WFLTF(driver)
    return driver.find_element_by_xpath('//body').get_attribute('innerHTML')


def actually_paste_comments(driver, rowNumber, comment, current_row_name):
    new_raport_test_status = driver.find_element_by_xpath(
        '//*[@id="SummaryResultResultsTableRouteGridName"]/div[4]/table/tbody/tr[' + str(rowNumber) + ']/td[7]').text
    current_comment = driver.find_element_by_xpath(
        '//*[@id="SummaryResultResultsTableRouteGridName"]/div[4]/table/tbody/tr[' + str(rowNumber) + ']/td[4]')
    if new_raport_test_status != 'PASSED' and new_raport_test_status != 'PASSED_WITH_WARNINGS':
        time.sleep(.2)
        print("pasting comment " + comment + ' at rowNumber ' + str(rowNumber))
        current_comment.click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="resultComment"]').clear()
        driver.find_element_by_xpath(
            '//*[@id="resultComment"]').send_keys(comment)
        driver.find_element_by_xpath('//*[@id="saveTextInputButton"]').click()
        WFLTF(driver)
    else:
        print(current_comment)
        print(current_row_name + " already has a comment!")


def copy_comments_from_a_test(driver, tests_with_comments):
    for test in tests_with_comments:
        for i in itertools.count():
            try:
                current_row_name = driver.find_element_by_xpath(
                    '//*[@id="SummaryResultResultsTableRouteGridName"]/div[4]/table/tbody/tr[' + str(1 + i) + ']/td[2]').text
                if(test[0] == (current_row_name)):
                    actually_paste_comments(
                        driver, 1 + i, test[1], current_row_name)
            except:
                break


def search_for_tests_with_comments(basicDataOldRaport):
    tests_with_comments = []
    for x in basicDataOldRaport:
        if(x[1] != " add " and x[1] != "Rerun passed  " and x[1] != "Kopia  "):
            tests_with_comments.append(x)
    return tests_with_comments


def copy_paste(driver, oldLink, newLink):
    html = get_html(driver, oldLink)
    basicDataOldRaport = scrapeBasicInfo.scrape_basic_info_from_raport(
        html, driver)
    driver.get(newLink)
    WFLTF(driver)
    time.sleep(3)

    tests_with_comments = search_for_tests_with_comments(basicDataOldRaport)

    copy_comments_from_a_test(driver, tests_with_comments)

    print("E L O")
    driver.quit()
