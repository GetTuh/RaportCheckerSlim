from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import importlib
ccLink = "https://commandcenter.igk.intel.com/Results/SummaryReport/2750499"
jiraChecker = importlib.import_module("jiraChecker")
jiraLinks = jiraChecker.getJiraLinks(ccLink)
driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
for x in jiraLinks:
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(x)
