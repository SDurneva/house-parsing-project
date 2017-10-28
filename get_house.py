import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_passport(link):
    """
    Prints out three pandas DataFrames based on information from the html got by link variable.
    First dataframe is made of two lists got by <div class:"numbered"> tags.
    Second and third dataframes are made of lists got by <div class:"grid"> tags.
    """
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    tabs = soup.find_all("div", {"class": "subtab"})
    info_numbered = []
    for subtab in tabs:
        info = subtab.find_all("div", {"class": "numbered"})
        for el in info:
            info_numbered.append(el)
    spans2 = []
    for el in info_numbered:
        spans1 = el.find_all("span")
        for el in spans1:
            spans2.append(el)
    del spans2[12], spans2[34], spans2[40]
    spans3 = []
    for el in spans2:
        spans3.append(el.text)
    spans = []
    for el in spans3:
        spans.append(re.sub('(  )+|\\n', '', el))
    left = spans[::2]
    right = spans[1::2]
    table = list(zip(left, right))
    print(pd.DataFrame(table))

    info_grid = []
    for subtab in tabs:
        info = subtab.find_all("div", {"class": "grid"})
        for el in info:
            info_grid.append(el)
    left_grid1_1 = []
    for el in info_grid:
        left = el.find_all("th", {"style": "text-align: center"})
        for el in left:
            left_grid1_1.append(el)
    del left_grid1_1[-1]
    right_grid1 = []
    for el in info_grid:
        right = re.findall('<td class=\"\">(.*?)<', str(el))
        for el in right:
            right_grid1.append(el)
    left_grid1 = []
    for el in left_grid1_1:
        left_grid1.append(el.text)
    table1 = list(zip(left_grid1, right_grid1))
    print(pd.DataFrame(table1))


    table1 = tabs[3].find("table", {"class": "orders overhaul-services-table"})
    rows_table1 = []
    rows_table1.append([el.text for el in table1.thead.find_all('th')])
    del table1[0]
    list1 = table1.find_all('tbody')
    for el in list1:
        list2 = [el1.text for el1 in el.find_all('td')]
        rows_table1.append(list2)
    print(pd.DataFrame(rows_table1))
