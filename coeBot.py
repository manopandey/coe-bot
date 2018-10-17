from datetime import datetime
from time import sleep
from os import environ
from bs4 import BeautifulSoup
import requests, pytz
import telegram

timezone = pytz.timezone('Asia/Singapore')

def result(rows, column, bidInfoBig):
    for n, i in enumerate(column):
        column[n] = i.text

    column.insert(0, "Code")
    CategoryCode_index = column.index('Code')
    Category_index = column.index('Category')
    try:
        QuotaPremium_index = column.index('QP($)')
    except:
        QuotaPremium_index = column.index('Current COE Price ($)')
    
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

    return (bidInfoBig+"\nCAT "+catA+"\nCAT "+catB+"\nCAT "+catC+"\nCAT "+catD+"\nCAT "+catE+"\n")


if __name__ == '__main__':
    bot = telegram.Bot(token=environ['TELEGRAM_TOKEN'])
    lastBroadcast = None
    while True:
        try:
            data = requests.get("https://www.mytransport.sg/oneMotoring/coeDetails.html").content
            soup = BeautifulSoup(data,"html.parser")
            rows = soup.find("table",{"class":"table_standard_type2"}).find("tbody").find_all("tr")
            column = soup.find("table",{"class":"table_standard_type2"}).find("thead").find("tr").find_all("th")
            bidInfo = soup.find("div",{"id":"subpage_content"}).find("p").text
            bidInfoBig = soup.find("div",{"id":"subpage_content"}).find("h3").text
            bidInfo_array = bidInfo.split()
            currentTime = datetime.now(timezone).strftime('%d%m%y%H%M')
            if 'finalised' in bidInfo_array:
                bidEnd = datetime.strptime(bidInfo_array[-7]+" "+bidInfo_array[-6], "%d/%m/%Y %H:%M").strftime('%d%m%y%H%M')
            else:
                bidEnd = datetime.strptime(bidInfo_array[-3]+" "+bidInfo_array[-2], "%d/%m/%Y %H:%M").strftime('%d%m%y%H%M')

            if 'has' and 'ended' in bidInfo_array:
                if lastBroadcast == None or lastBroadcast < currentTime:
                    if(currentTime == bidEnd):
                        bot.send_message('@getUpdateAndInfo', text=result(rows, column, bidInfoBig))
                        lastBroadcast = datetime.now(timezone).strftime('%d%m%y%H%M')
                else:
                    print("Bidding has ended")

                
            elif 'will' and 'end' in bidInfo_array:
                print("Bidding is currently in progress and will end on " + bidInfo_array[-3]+" "+bidInfo_array[-2])
            
            sleep(10)
        except:
            print("Error on COE page")
            sleep(10)

