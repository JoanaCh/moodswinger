from bs4 import BeautifulSoup
import requests

class music_control:
    def __init__(self):
        self.url = "https://www.internet-radio.com/stations/"
        self.genres = []
        self.genre_radios = []

        self.get_radios()

    def get_radios(self):
        soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        x = 0
        for i in soup.find_all("dt"):#("div", class_="container"):#.find_all("div", class_="row").find("div", class_=("col-md-4")).find_all("dl"):
            #print(i.a['href'])
            #print(i.a.string)
            self.genres.append([i.a['href'], i.a.string])

            #for b in i.find("a"):
                #print(b)
                #print(b.a)
    def get_genre_radios(self, radio_url):
        self.genre_radios = []
        url = "{0}{1}".format("https://www.internet-radio.com", radio_url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        for i in soup.find_all("table", class_="table table-striped")[0].find_all("tr"):
            list_radio = []
            a = i.find_all("td")[1].find_all("div")[1].find_all("i")[0].get('onclick').split(",")
            b = i.find_all("td")[2].find_all("h4")
            
            for x in b:
                list_radio.append(x.string)
            for x in a:
                if x.lstrip().startswith("\'http://") or x.lstrip().startswith("\'https://"):
                    list_radio.append(x[2:len(x)-3])

            self.genre_radios.append(list_radio)




#teste = music_control()
#teste.get_genre_radios("/stations/smooth%20jazz/")
#print(teste.genre_radios)

