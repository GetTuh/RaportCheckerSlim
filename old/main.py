from tkinter import *
import importlib
from selenium import webdriver
import pyperclip
# modules=["browser_script","jiraChecker",'clearAllComments','compareReports']

# for module in modules:
#     globals()['' % module]=importlib.import_module(module)


browser_script = importlib.import_module("browser_script")
jiraChecker = importlib.import_module("jiraChecker")
commentClear = importlib.import_module('clearAllComments')
compareReports = importlib.import_module('compareReports')
pasteCommentsToNewRaport = importlib.import_module('pasteCommentsToNewRaport')
justPaste = importlib.import_module('justPaste')

browser = 'Chrome'


def pasteFromClipboard(oldOrNew):
    if(oldOrNew == 'old'):
        OldRaport.delete(1.0, END)
        OldRaport.insert(1.0, pyperclip.paste())
    else:
        NewRaport.delete(1.0, END)
        NewRaport.insert(1.0, pyperclip.paste())


browserpath = ''
root = Tk()
w = Label(root, text="Stary raport: ")
w.pack()
OldRaport = Text(root, height=2, width=50)
pasteClipboardOld = Button(root, height=1, cursor="circle", bg='white', fg='black', width=20, text="Wklej ze schowka STARY",
                           command=lambda: pasteFromClipboard('old'))
pasteClipboardOld.pack()
OldRaport.pack()

w = Label(root, text="Nowy raport: ")
w.pack()
NewRaport = Text(root, height=2, width=50)
pasteClipboardNew = Button(root, height=1, cursor="circle", bg='white', fg='black', width=20, text="Wklej ze schowka NOWY",
                           command=lambda: pasteFromClipboard('new'))
pasteClipboardNew.pack()
NewRaport.pack()
raportArray = []


def compare_and_copy_comments():
    raportArray.append(OldRaport.get("1.0", "end-1c"))
    raportArray.append(NewRaport.get("1.0", "end-1c"))
    JiraCheck = var.get()
    root.destroy()
    start(JiraCheck)


def clear_comments():
    raportArray.append(NewRaport.get("1.0", "end-1c"))
    root.destroy()
    commentClear.deleteComments(raportArray[0])

buttonCommit = Button(root, height=1, cursor="circle", bg='green', fg='black', width=15, text="Przeklej komentarze",
                      command=lambda: compare_and_copy_comments())
buttonCommit.pack()
button2 = Button(root, height=1, width=30, cursor='shuttle', bg='blue', fg='white', text="Tylko sprawdź stan jir w nowym raporcie ",
                 command=lambda: jira_check())
button2.pack()

button3 = Button(root, height=1, width=30, bg='brown', cursor='pirate', fg='white', text="Wyczyść komentarze z nowego raportu",
                 command=lambda: clear_comments())
button3.pack()


button4 = Button(root, height=2, width=40, cursor="heart", bg="red", text="Przeklej wszystkie komentarze na ślepo (Marek Ficzer) \n !!!NADPISUJE WSZYSTKIE KOMENTARZE!!!",
                 command=lambda: marekFiczer())
button4.pack()

w = Label(root, text="")
w.pack()
var = IntVar()

c = Checkbutton(
    root, text="Sprawdź stan jir w nowym raporcie po przeklejeniu komentarzy", variable=var)
c.pack()


def start(JiraCheck):

    driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")

    print("Getting data from old raport...\nLaunching browser")

    oldRep = browser_script.main(driver, raportArray[0], "old", [])
    print("Getting data from new raport...\nLaunching browser")
    newRep = browser_script.main(driver, raportArray[1], "new", oldRep)

    print("Comparing reports...")
    newlist = compareReports.compareReports(oldRep, newRep)
    print("Pasting reports...")
    pasteCommentsToNewRaport.pasteCommentsToNewRaport(
        driver, newlist, raportArray[1])
    driver.quit()


def jira_check():
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
    raportArray.append(NewRaport.get("1.0", "end-1c"))
    root.destroy()
    jiraLinks = jiraChecker.getJiraLinks(raportArray[0], driver)
    jiraChecker.checkJiras(jiraLinks, driver)


def marekFiczer():

    driver = webdriver.Chrome("C:\Program Files (x86)\Google\chromedriver.exe")
    oldRaportLink = (OldRaport.get("1.0", "end-1c"))
    newRaportLink = (NewRaport.get("1.0", "end-1c"))
    root.destroy()
    justPaste.copy_paste(driver, oldRaportLink, newRaportLink)

mainloop()
