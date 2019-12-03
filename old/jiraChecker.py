from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import array
from bs4 import BeautifulSoup
import re
import importlib

waitForLoadToFinish = importlib.import_module("waitForLoadingToFinish")


def WFLTF(driver):
    waitForLoadToFinish.waitForLoadToFinish(driver)


def getJiraLinks(link, driver):
    try:
        driver.get(link)
        time.sleep(.4)
        driver.find_element_by_xpath(
            '//*[@id="SummaryResultResultsTableRouteGridName"]/div[5]/span[1]/span/span').click()
        time.sleep(.4)
        driver.find_element_by_xpath(
            "//li[contains(@class, 'k-item')][7]").click()
        WFLTF(driver)
    except Exception as e:
        print(e)
        driver.quit()
        print("Coś nie działa elo jedziemy jeszcze raz")
        driver = webdriver.Chrome(
            "C:\Program Files (x86)\Google\chromedriver.exe")
        main(link)

    html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find_all(class_='commentCell')
    links = []
    regexp = re.compile(r'jira\.devtools\.intel\.com')
    for z in range(len(soup)):
        x = soup[z]
        x = ''.join(x.findAll(text=True))
        allLinks = (re.findall(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", x))
        for y in allLinks:
            if regexp.search(y):
                links.append(y)
            else:
                print(y + " nie jest linkiem do jiry")

    links = list(dict.fromkeys(links))
    return links


def checkJiras(links, driver):
    closedJiras = []
    tabNr = 1
    for x in links:
        z=False
        driver.get(x)
        while True:
            try:
                status = driver.find_element_by_class_name(
                    'jira-issue-status-lozenge').text
                break
            except:
                if(z==False):
                    print("Jira działa tak wolno że program by już nie działał! eh. Czekamy")
                    z=True
                else:
                    print("czekamy dalej")
                time.sleep(3)

        print("Status: " + status)
        if status == "CLOSED" or status == "RESOLVED":
            closedJiras.append(x + " - " + status)
            driver.execute_script("window.open('');")
            # Switch to the new window and open URL B
            driver.switch_to.window(driver.window_handles[tabNr])
            tabNr += 1

    print("Jiras to check:")
    for x in closedJiras:
        print(x)
    driver.close()
    input("Wcisnij enter aby wyjsc...")
