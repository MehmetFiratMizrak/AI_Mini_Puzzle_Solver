from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

delay_time = 2
chromeDriver = webdriver.Chrome(ChromeDriverManager().install())


def _dab(path, delay_time):  # This function used for click to defined path with specified delay
    chromeDriver.find_element_by_xpath(path).click()
    time.sleep(delay_time)


def Convert(string):
    li = list(string.split(" "))
    return li


def _goWikipediaPage(aList):

    chromeDriver.get('https://en.wikipedia.org/wiki/Main_Page')
    search_box = chromeDriver.find_element_by_name("search")
    search_box.send_keys(aList)
    search_box.submit()
    try:

        _dab("/html/body/div[3]/div[3]/div[4]/div[4]/p[2]/a[5]", delay_time)  # 250 results per page

        element = chromeDriver.find_element_by_xpath("/html/body/div[3]/div[3]/div[4]/div[4]/ul")
        List = Convert(element.text)

    except:
        element = chromeDriver.find_element_by_xpath("/html/body/div[3]/div[3]")
        List = Convert(element.text)

    newList = list()
    x = len(List)
    i = 0
    for singleList in List:
        if len(singleList) > 2 and len(singleList) < 6:
            newList.append(singleList)
            print(len(singleList))
        """"    
        a = len(List[i])
        if (a < 3 or a > 5):
            List.pop(i)
            x = x -1
        i = i + 1
        """
    print(len(newList))
    return newList


mylist = ["ali", "Count at the gym", "Springsteen's podcast partner on 'Renegades: Born in the U.S.A.'",
          "Italian fashion hub",
          "Watchful for possible danger", "A ton", "Tomato type", "Online way to pay utilities",
          "Kind of diet that mimics cavemen",
          "Modern lead-in to phone, TV and even refrigerator", "___ on a log (celery snack)"]

print(_goWikipediaPage(mylist[4]))
