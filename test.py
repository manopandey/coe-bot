from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pytz


data = requests.get("https://www.mytransport.sg/oneMotoring/coeDetails.html")
content = data.content

soup = BeautifulSoup(content,"html.parser")
if(soup.find("div",{"class":"privacy_content"}).find("div").text == "System Maintenance in Progress"):
    print(True)
else:
    print(False)
# bidDate = soup.find("div",{"id":"subpage_content"}).find("h3").text

# bidEnd = soup.find("div",{"id":"subpage_content"}).find("p").text
# bidEnd_DateTime = int(bidEnd.find("/"))-2

# coe_new = soup.find("table",{"class":"table_standard_type2"}).find("tbody").find_all("tr")

# catA = coe_new[0].find_all("td")
# catB = coe_new[1].find_all("td")
# catC = coe_new[2].find_all("td")
# catD = coe_new[3].find_all("td")
# catE = coe_new[4].find_all("td")

# if catA[2].text == "1":
#     print ("Bidding is currently in progress, Please check back after "+bidEnd[bidEnd_DateTime:])
# else:
#     print (bidDate+"\nCAT "+catA[0].text+" - "+catA[1].text+" - $"+catA[3].text+"\nCAT "+catB[0].text+" - "+catB[1].text+" - $"+catB[3].text+"\nCAT "+catC[0].text+" - "+catC[1].text+" - $"+catC[3].text+"\nCAT "+catD[0].text+" - "+catD[1].text+" - $"+catD[3].text+"\nCAT "+catE[0].text+" - "+catE[1].text+" - $"+catE[3].text+"\n")



