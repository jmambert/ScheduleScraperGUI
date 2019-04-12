# necessary modules

# getting paging and scraping
import bs4
import requests
import random
from openpyxl import load_workbook

# analysis of scraped data
import pandas as pd

def infoFunction():
    # set data that necessary for request
    # url
    base_url = "https://banner.umw.edu/prod/umw_clas.p_displayallnocount"

    # headers of POST request
    headers = {
            "Host": "banner.umw.edu",
            "Connection": "keep-alive",
            "Content-Length": 79,
            "Cache-Control": "max-age=0",
            "Origin": "https://banner.umw.edu",
            "Upgrade-Insecure-Requests": 1,
            "DNT": 1,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.65",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Referer": "https://banner.umw.edu/prod/umw_clas.p_displayallnocount",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
            }

    # body of POST request
    data = {
            "call_proc_in": "umw_clas.p_displayallnocount",
            "term_in": 201908,
            "coll_in": "%",
            "levl_in": "UG",
            }

    # make request to server and get page
    page = requests.post(base_url, data, headers).text

    # convert page to soup
    soup = bs4.BeautifulSoup(page, 'html.parser')

    # substitute all break-tags with newlines
    for x in soup.find_all('br'):
        x.replace_with('\n')

    # get table with all courses data
    table = soup.find('table', class_="datadisplaytable")

    # these are indices of columnts that we will need
    COURSE, SECTION, TIME, DAYS, ROOM, INSTRUCTOR = 1, 2, 10, 11, 14, 15


    classes_data = []

    # iterate through all rows
    for row in table.find_all('tr'):
        if row.find('th'):  # if header row -- discard it
            continue

        # substitue all '\xa0' for simple empty spaces
        row_data = [x.text.replace('\xa0', ' ') for x in row.find_all('td')]

        # extract all data. `.rstrip` to get rid of newlines on the right
        course, section, time = row_data[COURSE], row_data[
                SECTION], row_data[TIME].rstrip()
        days, room, instructor = row_data[DAYS].rstrip(), row_data[
                ROOM].rstrip(), row_data[INSTRUCTOR].rstrip()

        # some lines have two lines for same course if they are held at different times
        # if we encounter such line, we split it in two and save both
        if '\n' in time:
            time1, time2 = time.split('\n')
            days1, days2 = days.split('\n')
            room1, room2 = room.split('\n')

            # here we save 4 items
            # instructor name, course name with section, time with day of week,
            # room
            row1 = [instructor, course + '-' + section, time1 + f' ({days1})', room1]
            row2 = [instructor, course + '-' + section, time2 + f' ({days2})', room2]

            classes_data.append(row1)
            classes_data.append(row2)

        # otherwise we only save single line
        else:
            row = [instructor, course + '-' + section, time + f'({days})', room]
            classes_data.append(row)

    all_classes_data = classes_data

    # create pandas dataframe with all the data
    classes_data = pd.DataFrame(classes_data, columns=(
        "Instructor", "Course", "Time", "Room"))

    # select data with desired courses (i.e. CPSC, CYBR, DATA)
    # technically, this could also be done earlier in the scraping loop
    mask = (classes_data.Course.str.contains('DATA') |
            classes_data.Course.str.contains('CYBR') |
            classes_data.Course.str.contains('CPSC'))
    data = classes_data[mask]

    # write data to excel file
    #Create a pandas excel writer using xlsx writer as the engine
    writer = pd.ExcelWriter("Semester Schedule.xlsx", engine='xlsxwriter')

    # setting index allows pandas to merge some cells automatically when writing
    data.set_index(['Instructor', 'Course']
            ).sort_index().to_excel(writer, sheet_name='Semester Schedule')

    #Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Semester Schedule']

    #set the column width
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 25)

    writer.save()

    return classes_data

def grabData():
    # set data that necessary for request
    # url
    base_url = "https://banner.umw.edu/prod/umw_clas.p_displayallnocount"

    # headers of POST request
    headers = {
            "Host": "banner.umw.edu",
            "Connection": "keep-alive",
            "Content-Length": 79,
            "Cache-Control": "max-age=0",
            "Origin": "https://banner.umw.edu",
            "Upgrade-Insecure-Requests": 1,
            "DNT": 1,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.65",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Referer": "https://banner.umw.edu/prod/umw_clas.p_displayallnocount",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
            }

    # body of POST request
    data = {
            "call_proc_in": "umw_clas.p_displayallnocount",
            "term_in": 201908,
            "coll_in": "%",
            "levl_in": "UG",
            }

    # make request to server and get page
    page = requests.post(base_url, data, headers).text

    # convert page to soup
    soup = bs4.BeautifulSoup(page, 'html.parser')

    # substitute all break-tags with newlines
    for x in soup.find_all('br'):
        x.replace_with('\n')

    # get table with all courses data
    table = soup.find('table', class_="datadisplaytable")

    # these are indices of columnts that we will need
    COURSE, SECTION, TIME, DAYS, ROOM, INSTRUCTOR = 1, 2, 10, 11, 14, 15


    classes_data = []

    # iterate through all rows
    for row in table.find_all('tr'):
        if row.find('th'):  # if header row -- discard it
            continue

        # substitue all '\xa0' for simple empty spaces
        row_data = [x.text.replace('\xa0', ' ') for x in row.find_all('td')]

        # extract all data. `.rstrip` to get rid of newlines on the right
        course, section, time = row_data[COURSE], row_data[
                SECTION], row_data[TIME].rstrip()
        days, room, instructor = row_data[DAYS].rstrip(), row_data[
                ROOM].rstrip(), row_data[INSTRUCTOR].rstrip()

        # some lines have two lines for same course if they are held at different times
        # if we encounter such line, we split it in two and save both
        if '\n' in time:
            time1, time2 = time.split('\n')
            days1, days2 = days.split('\n')
            room1, room2 = room.split('\n')

            # here we save 4 items
            # instructor name, course name with section, time with day of week,
            # room
            row1 = [instructor, course + '-' + section, time1 + f' ({days1})', room1]
            row2 = [instructor, course + '-' + section, time2 + f' ({days2})', room2]

            classes_data.append(row1)
            classes_data.append(row2)

        # otherwise we only save single line
        else:
            row = [instructor, course + '-' + section, time + f'({days})', room]
            classes_data.append(row)
    return classes_data
