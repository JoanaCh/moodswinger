from bs4 import BeautifulSoup
import requests

class music_control:


    def __init__(self):
        self.url = "https://www.internet-radio.com/stations/"
        self.genres = []
        #self.genre_radios = []

        self.json_genres ={}

        self.json_genres["Alternative"] =["alternative", "adult contemporary", "anime", "breakcore", "dancepunk", "darkwave", "emo", "experimental", "game", "grindcore", "happy hardcore", "hardcore", "hardstyle", "indie", "industrial", "new age", "new wave", "progressive", "psychedelic"]
        self.json_genres["Calm"] = ["lounge", "ambient", "chill", "chillout", "downtempo", "easy listening", "healing", "instrumental", "meditation", "minimal", "nature", "relaxation", "religious"]
        self.json_genres["Classical"] = ["classical", "baroque", "chamber", "christian", "opera", "orchestra", "piano", "romantic"]
        self.json_genres["Dance"] = ["dance", "caribbean", "cumbia", "dancehall", "disco", "eurodance", "funk", "jumpstyle", "kizomba", "merengue", "mixtapes", "reggaeton", "salsa", "sport"]
        self.json_genres["Electronic"] = ["electronic", "acid house", "bass", "bass house", "breakbeat", "breaks", "complextro", "deep house", "drone", "drum and bass", "dub", "dubstep", "ebm", "edm", "electro", "electro house", "electronica", "fidget house", "fusion", "gabber", "goa", "grime", "hard house", "hard trance", "hardtechno", "house", "idm", "makina", "moombahton", "neurofunk", "neurohop", "noise", "psybient", "psybreaks", "psychobilly", "psytrance", "rave", "schranz", "space", "speedcore", "synthpop", "tech house", "techno", "technology", "tekno", "trance", "trap"]
        self.json_genres["Folk"] = ["folk", "americana", "bhangra", "bluegrass", "bollywood", "calypso", "celtic", "chinese", "country", "desi", "flamenco", "greek", "hindi", "indian", "irish", "japanese", "jewish", "latin", "manele", "polka", "romania", "schlager", "soca", "spanish", "tejano", "thai", "tribal", "world", "vocal", "western swing"]
        self.json_genres["Gospel"] = ["gospel", "african", "spiritual"]
        self.json_genres["HipHop"] = ["hip hop", "big beat", "dirty south", "east coast", "freestyle", "glitch hop", "jungle", "rap", "rnb", "soul", "trip hop", "urban", "west coast", "zouk"]
        self.json_genres["Jazz"] = ["jazz", "big band", "blues", "doo wop", "exotica", "nu jazz", "skiffle", "smooth jazz", "swing"]
        self.json_genres["Pop"] = ["pop", "50s", "60s", "70s", "80s", "90s", "baladas", "britpop", "christmas", "decades", "europop", "jpop", "kpop", "mor", "showtunes", "soundtracks", "talk", "top 40"]
        self.json_genres["Rock"] = ["rock", "classic rock", "garage", "glam rock", "goth", "gothic", "grunge", "heavy metal", "jrock", "metal", "oldies", "punk", "rockabilly", "roots", "surf"]
        self.json_genres["Reggae"] = ["reggae", "ragga", "ska"]
        self.json_genres["Others"] = ["comedy", "community", "news"]

        #self.get_radios()

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
        #self.genre_radios = []
        url = "{0}{1}/".format("https://www.internet-radio.com/stations/", radio_url)
        print(url)
        print(radio_url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        lista_send = []
        for i in soup.find_all("table", class_="table table-striped")[0].find_all("tr"):
            list_radio = []
            a = i.find_all("td")[1].find_all("div")[1].find_all("i")[0].get('onclick').split(",")
            b = i.find_all("td")[2].find_all("h4")
            
            
            for x in b:
                list_radio.append(x.string)

            for x in a:
                if x.lstrip().startswith("\'http://") or x.lstrip().startswith("\'https://"):
                    list_radio.append(x[2:len(x)-3])

            lista_send.append(list_radio)
            #self.genre_radios.append(list_radio)

        return lista_send




#teste = music_control()
#x = teste.get_genre_radios("smooth%20jazz")
#print(x)

