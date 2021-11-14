import requests
from bs4 import BeautifulSoup as bs
import time
import random
import json
import os

def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    return requests.get(url=url, headers=headers)


def timer():
    time.sleep(random.uniform(3, 5))


k = "\""
p = ""
dv = ":"
dk = "<<"
dkk = ">>"
data = []
url = 'https://edu.tatar.ru'
if not os.path.exists("Data/regionsPage.html"):
    fl = True
    while fl:
        try:
            request = get_data(url + '/index.htm')
            fl = False
        except Exception:
            time.sleep(15)

    with open("Data/regionsPage.html", 'w', encoding='utf-8') as file:
        file.write(request.text)
with open("Data/regionsPage.html", 'r', encoding='utf-8') as file:
    regionsPage = bs(file.read(), 'lxml')

regions = []
for i in regionsPage.find_all("ul", class_="edu-list"):
    regions.append(i.find_all("a"))
data = []
for regionsList in regions:
    for region in regionsList:
        regionName = region.text
        regionPageAddress = region.get("href")

        if not os.path.exists(f"Data/{regionName}"):
            os.mkdir(f"Data/{regionName}")

        if not os.path.exists(f"Data/{regionName}/regionPage.html"):
            timer()
            fl = True
            while fl:
                try:
                    regionReq = get_data(url + regionPageAddress + '/type/1')
                    fl = False
                except Exception:
                    time.sleep(15)
            with open(f"Data/{regionName}/regionPage.html", 'w', encoding='utf-8') as file:
                file.write(regionReq.text)
        with open(f"Data/{regionName}/regionPage.html", 'r', encoding='utf-8') as file:
            regionPage = bs(file.read(), 'lxml')

        for ul in regionPage.find_all("ul", class_="edu-list col-md-4"):
            for school in ul.find_all("a"):
                schoolName = school.text
                schoolAddress = ""
                schoolPhoneNumber = ""
                schoolEmail = ""

                print(f"{regionName} район, {schoolName}")
                
                bsl = "/"
                sl = "\\"
                if not os.path.exists(f"Data/{regionName}/{schoolName.replace(k, p).split(bsl)[0].strip().replace(dv, p).replace(dk, p).replace(dkk, p).replace(sl, p)}"):
                    os.mkdir(f"Data/{regionName}/{schoolName.replace(k, p).split(bsl)[0].strip().replace(dv, p).replace(dk, p).replace(dkk, p).replace(sl, p)}")

                if not os.path.exists(f"Data/{regionName}/{schoolName.replace(k, p).split(bsl)[0].strip().replace(dv, p).replace(dk, p).replace(dkk, p).replace(sl, p)   }/schoolPage.html"):
                    timer()
                    fl = True
                    while fl:
                        try:
                            schoolReq = get_data(url + school.get("href"))
                            fl = False
                        except Exception:
                            time.sleep(15)
                    with open(f"Data/{regionName}/{schoolName.replace(k, p).split(bsl)[0].strip().replace(dv, p).replace(dk, p).replace(dkk, p).replace(sl, p)}/schoolPage.html", 'w', encoding='utf-8') as file:
                        file.write(schoolReq.text)
                with open(f"Data/{regionName}/{schoolName.replace(k, p).split(bsl)[0].strip().replace(dv, p).replace(dk, p).replace(dkk, p).replace(sl, p)}/schoolPage.html", 'r', encoding='utf-8') as file:
                    schoolPage = bs(file.read(), 'lxml')

                schoolContactBlock = schoolPage.find("div", class_="sp_block contacts")
                for td in schoolContactBlock.find_all("tr"):
                    if td.find("strong").text.strip() == "Адрес:":
                        schoolAddress = td.find_all("td")[1].text.strip()
                    if td.find("strong").text.strip() == "Телефон:":
                        schoolPhoneNumber = td.find_all("td")[1].text.strip()
                    if td.find("strong").text.strip() == "E-Mail:":
                        schoolEmail = td.find_all("td")[1].text.strip()

                data.append({
                    "Район": regionName,
                    "Школа": schoolName,
                    "Номер": schoolPhoneNumber,
                    "Почта": schoolEmail,
                    "Адрес": schoolAddress
                })
with open("data.json", "a", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
