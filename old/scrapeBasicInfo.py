from bs4 import BeautifulSoup


def scrape_basic_info_from_raport(html, OldOrNew):
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find_all(role='rowgroup')[5]
    soup = soup.findAll("tr", {"data-uid": True})
    all_data = []
    for x in range(len(soup)):
        for z in range(13):
            arr = soup[x].findAll('td')
            if z == 2:
                count = x + 1
                print("count: " + str(count))
                name = arr[z].text
                print("name: " + name)
            if z == 3:
                comment = arr[z].text
                print("comment: " + str(comment.encode("utf-8")))
            if z == 6:
                fail_or_pass = arr[z].text
                print("Result: " + fail_or_pass)
                try:
                    log_link = arr[z].a.get('href')
                    print("Log link: " + log_link)
                except:
                    print(name + " has no log link!")
                    log_link = False

        if((comment != "add" and comment != 'Kopia') or OldOrNew == "new"):
            print(count)
            all_data.append([name, comment, fail_or_pass, log_link])
    return(all_data)
