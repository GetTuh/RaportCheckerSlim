from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import array
from bs4 import BeautifulSoup
import importlib
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

startsWithErrorMessageToSkip = ['TestFailureException',
                                'System.',
                                'Last Virtual Terminal screen',
                                '  Not all messages were found!',
                                'Test failed on TraceSearch!',
                                'Exception message',
                                '  Found pattern:',
                                '  Setup configuration',
                                'Boot to BIOS Setup Menu',
                                'Successfully booted to BIOS Setup Menu',
                                'Waiting for BDS prompts and performing key press',
                                'Exception occured on prepare stage',
                                'Prepare test setup',
                                'Run test']


waitForLoadToFinish = importlib.import_module("waitForLoadingToFinish")


def WFLTF(driver):
    waitForLoadToFinish.waitForLoadToFinish(driver)


def main(driver, link, OldOrNew, oldRep):
    try:
        driver.get(link)
        print(OldOrNew)
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="SummaryResultResultsTableRouteGridName"]/div[5]/span[1]/span/span').click()
        time.sleep(.4)
        driver.find_element_by_xpath(
            "//li[contains(@class, 'k-item')][7]").click()
        WFLTF(driver)
        time.sleep(2)
    except Exception as e:
        print(e)
        driver.quit()
        print("Coś nie działa elo jedziemy jeszcze raz")
        driver = webdriver.Chrome(
            "C:\Program Files (x86)\Google\chromedriver.exe")
        main(driver, link, OldOrNew, oldRep)

    try:
        if(oldRep[0] != null and OldOrNew == "old"):
            print(oldRep[0])
            print("Haha,mam cię błądzie elo")
            print("Getting data from new raport...\nLaunching browser")
            newRep = main(driver, 'new', oldRep)
    except:
        print("A-ok")

    def returnTableData(trNum, tdNum):
        xpath_driver = driver.find_element_by_xpath(
            "//*[@id=\"SummaryResultResultsTableRouteGridName\"]/div[4]/table/tbody/tr[" + str(trNum) + "]/td[" + str(tdNum) + "]")
        return (xpath_driver)

    def returnLogLink(trNum):
        try:
            return driver.find_element_by_xpath("//*[@id=\"SummaryResultResultsTableRouteGridName\"]/div[4]/table/tbody/tr[" + str(trNum) + "]/td[7]/a[1]").get_attribute("href")
        except:
            print("Nie ma linku do raportu! haha x d ")

    def findErrors(allErrors, failType):
        errors = []
        for x in allErrors:
            x = x.get_attribute('innerHTML')
            soup = BeautifulSoup(x, 'html.parser')
            if not soup.find('passed'):
                for z in soup.find_all(class_='content'):
                    z = ''.join(z.findAll(text=True))
                    errors.append(z)
                    print(z)
        return errors

    def returnFailureSkipOrTestError(FailSkipError):
        return{
            'FAILED': findErrors(driver.find_elements_by_xpath("//div[contains(@class, 'message') and contains(@class, 'failure')]"), 'FAILED'),
            # ZEPSUTE - Nie szuka wszystkich problemów, do przeróbki
            'SKIPPED': findErrors(driver.find_elements_by_xpath("//div[contains(@class, 'message') and contains(@class, 'skipped')]"), 'SKIPPED'),
            'TEST_ERROR': findErrors(driver.find_elements_by_xpath("//div[contains(@class, 'message') and contains(@class, 'exception')]"), 'TEST_ERROR')
        }[FailSkipError]

    try:
        howManyTests = (len(driver.find_elements_by_xpath(
            "//*[@id=\"SummaryResultResultsTableRouteGridName\"]/div[4]/table/tbody/tr")))
    except Exception as e:
        print(e)
        driver.quit()
        main(link, OldOrNew, oldRep)

    def addTestsToArray(arraySourceReport):

        for x in range(1, howManyTests + 1):
            testComment = returnTableData(x, 4).text
            if((testComment != "add" and testComment != "Kopia")or OldOrNew == "new"):
                testName = returnTableData(x, 2).text
                print("TEStING " + testName)
                # if(testName=="DisableEopAndCbd"):
                if(OldOrNew == "new"):
                    for items in oldRep:  # TODO: BS4 zamiast selenium
                        if(items[0] == testName):
                            arraySourceReport.insert(
                                x, [(testName), (testComment), (returnTableData(x, 7).text), returnLogLink(x)])
                            print("Adding " + testName + " test...")
                else:
                    arraySourceReport.insert(
                        x, [(testName), (testComment), (returnTableData(x, 7).text), returnLogLink(x)])
                    print("Adding " + testName + " test...")
    arraySourceReport = []
    addTestsToArray(arraySourceReport)
    # todo: remove doubles
    for x in arraySourceReport:
        if((x[2] == "FAILED" or x[2] == "SKIPPED" or x[2] == "TEST_ERROR")) and ((x[1] != "add" and x[1] != "Kopia")or OldOrNew == "new"):
            driver.find_element_by_tag_name(
                'body').send_keys(Keys.COMMAND + 't')
            try:
                driver.get(x[3])
                time.sleep(.2)
                driver.find_element_by_xpath(
                    '//*[@id="switches"]/div[1]/label').click()  # expanding groups
                time.sleep(.4)
                failures = returnFailureSkipOrTestError(x[2])
                for z in failures:
                    toAdd = True
                    print(z)
                    for itemz in startsWithErrorMessageToSkip:
                        if z.startswith(itemz):
                            toAdd = False
                            print("... error skipped")
                    if toAdd:
                        x.append(z)
            except:
                print("URL nie jest stringiem.... prawdopodobnie xD")
            driver.find_element_by_tag_name(
                'body').send_keys(Keys.COMMAND + 'w')
    return arraySourceReport
