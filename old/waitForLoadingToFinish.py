from selenium import webdriver
import time


def waitForLoadToFinish(driver):
    while True:
        try:
            time.sleep(.3)
            driver.find_element_by_class_name('k-loading-image')
            time.sleep(.5)
            print("Loading...")
        except Exception as e:
            break
    time.sleep(.8)
