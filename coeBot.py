from datetime import datetime
from time import sleep
from os import environ
from bs4 import BeautifulSoup
import requests, pytz
import telegram

last_broadcast = None
#Set timezone incase server is not in singapore
timezone = pytz.timezone('Asia/Singapore')
global last_broadcast , timezone

def isBidding_broadcasted(soup):
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

    #Check if bid has been broadcasted or bidding is in progress
    if(last_broadcast > bidEnd_datetime or bidEnd_datetime > datetime.now(timezone)):
        return True
    else:
        return False
    

def main():
    #Request site, and extract content and save to variable
    site_content = requests.get("https://www.mytransport.sg/oneMotoring/coeDetails.html").content

    #Parse content using BeautifulSoup
    soup = BeautifulSoup(site_content,"html.parser")

    #Check if bidding is going on or data has been broadcasted
    if(isBidding_broadcasted(soup)):
        raise Exception('Bidding or Broadcasted !')
    else:
        #Latest bid period 
        bid_period = soup.find("div",{"id":"subpage_content"}).find("h3").text 
        #Latest Coe Results
        coe_new = soup.find("table",{"class":"table_standard_type2"}).find("tbody").find_all("tr")
        #Assign values to variables
        catA = coe_new[0].find_all("td")
        catB = coe_new[1].find_all("td")
        catC = coe_new[2].find_all("td")
        catD = coe_new[3].find_all("td")
        catE = coe_new[4].find_all("td")
        #Format and return response
        return(bid_period+"\nCAT "+catA[0].text+" - "+catA[1].text+" - $"+catA[3].text+"\nCAT "+catB[0].text+" - "+catB[1].text+" - $"+catB[3].text+"\nCAT "+catC[0].text+" - "+catC[1].text+" - $"+catC[3].text+"\nCAT "+catD[0].text+" - "+catD[1].text+" - $"+catD[3].text+"\nCAT "+catE[0].text+" - "+catE[1].text+" - $"+catE[3].text+"\n")


if __name__ == '__main__':
    bot = telegram.Bot(token=environ['TELEGRAM_TOKEN'])
    while True:
        try:
            bot.send_message('@getCoe', text=main())
            last_broadcast = datetime.now(timezone)
        except Exception as err:
            print(str(err))
        sleep(10)
