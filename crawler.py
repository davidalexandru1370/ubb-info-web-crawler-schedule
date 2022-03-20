import copy

import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup


# print("Titlu = " +  bsoup.title.string)


def main():
    URL = "https://www.cs.ubbcluj.ro/files/orar/2021-2/tabelar/IE1.html"

    browser = RoboBrowser(parser="html5lib")
    free_hours = ["7.30", "9.20", "11.10", "13.00", "14.50", "16.40", "18.30" ,"20.20"]
    days_of_week = ["Luni","Marti","Miercuri","Joi","Vineri"]
    subjects_to_skip = ["Metode avansate de rezolvare a problemelor de matematica si informatica",
                        "Fundamentele pedagogiei",
                        "Cerc de programare in C",
                        "Tutoriat"
                        ]
    days_and_hours = [[0 for x in range((len(free_hours)+1))] for y in range(len(days_of_week))]
    for row in range(len(days_of_week)):
        days_and_hours[row][0] = copy.copy(days_of_week[row])
    #print(days_and_hours[0][0])
    #print(days_and_hours[1][0])
    browser.open(URL)
    group = 916
    page = str(browser.parsed)
    bsoup = BeautifulSoup(page, "html5lib")
    index = 0
    for table in bsoup.find_all("table"):
        if index == (group % 10 - 1):
            rows = table.find_all("tr")
            for row in rows:
                elements = list()
                elements = row.find_all("td")
                text = list()
                for element in elements:
                    text.append(element.get_text())

                if len(text) > 0:
                    #print(text[0])
                    activity = text[1].split('-')

                    begin_hour = activity[0]
                    end_hour = activity[1]
                    if(text[4]!="916/2" and text[6] not in subjects_to_skip):

                        if begin_hour in free_hours:
                            hour_index = free_hours.index(str(begin_hour).strip())
                            day_index = days_of_week.index(text[0])
                            days_and_hours[day_index][hour_index+1] = 1
        index += 1

    for row in range(len(days_and_hours)):
        print(days_and_hours[row][0])
        for column in range(1,len(days_and_hours[0])):
            if days_and_hours[row][column] == 0:
                if column < len(days_and_hours[0])-1:
                    print(free_hours[column-1] + " - " + free_hours[column])
                else:
                    print(free_hours[column-1] + " - 00:00" )
        print("-"*100)
main()
