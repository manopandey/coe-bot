import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

timezone = pytz.timezone('Asia/Singapore')

def bidEnd(soup):
    #String returns last bid datetime, if bidding is on-going it will return bid end datetime 
    bidEnd = soup.find("div",{"id":"subpage_content"}).find("p").text

    #Position where date and time starts in "bidEnd" string
    bidEnd_date_startpos = int(bidEnd.find("/"))-2
    bidEnd_time_startpos = int(bidEnd.find(":"))-2

    #Using start positions, extract bid end date and time and store in variables
    bidEnd_date = bidEnd[bidEnd_date_startpos:bidEnd_time_startpos]
    bidEnd_time = bidEnd[bidEnd_time_startpos:bidEnd_time_startpos + 5]
    
    #Create datetime object using bid end date and time
    bidEnd_datetime = datetime.strptime(bidEnd_date+" "+bidEnd_time, "%d/%m/%Y %H:%M")
    #Convert to aware datetime object
    bidEnd_datetime = timezone.localize(bidEnd_datetime)

    return(bidEnd_datetime)



def coe():
    data = requests.get("https://www.mytransport.sg/oneMotoring/coeDetails.html").content

    soup = BeautifulSoup(data,"html.parser")

    rows = soup.find("table",{"class":"table_standard_type2"}).find("tbody").find_all("tr")
    column = soup.find("table",{"class":"table_standard_type2"}).find("thead").find("tr").find_all("th")
    bidInfo = soup.find("div",{"id":"subpage_content"}).find("h3").text

    for n, i in enumerate(column):
        column[n] = i.text

    column.insert(0, "Code")
    CategoryCode_index = column.index('Code')
    Category_index = column.index('Category')
    QuotaPremium_index = column.index('QP($)')

    catA = rows[0].find_all("td")
    catB = rows[1].find_all("td")
    catC = rows[2].find_all("td")
    catD = rows[3].find_all("td")
    catE = rows[4].find_all("td")

    catA = catA[CategoryCode_index].text+" - "+catA[Category_index].text+" - $"+catA[QuotaPremium_index].text
    catB = catB[CategoryCode_index].text+" - "+catB[Category_index].text+" - $"+catB[QuotaPremium_index].text
    catC = catC[CategoryCode_index].text+" - "+catC[Category_index].text+" - $"+catC[QuotaPremium_index].text
    catD = catD[CategoryCode_index].text+" - "+catD[Category_index].text+" - $"+catD[QuotaPremium_index].text
    catE = catE[CategoryCode_index].text+" - "+catE[Category_index].text+" - $"+catE[QuotaPremium_index].text

    return (bidInfo+"\nCAT "+catA+"\nCAT "+catB+"\nCAT "+catC+"\nCAT "+catD+"\nCAT "+catE+"\n")



print(coe())