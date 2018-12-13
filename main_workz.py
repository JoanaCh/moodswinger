from time import sleep, time                                # Para o tempo
import lcddriver                                            # Isto e para a informacao dada pelo LCD
import RPi.GPIO as GPIO                                     # GPIOS do raspberry
import music as mu                                          # Para os radios, para fazer web scrapping
import subprocess, os, signal                               # Criacao de sub processos
from bitalino import BITalino                               # Isto ja sera para o bitalino
import multiprocessing                                      # para os processos do texto

GPIO.setmode(GPIO.BCM)

"""
TODO:
    1  fazer menu para o bitalino
"""


class program:
    def __init__(self):
        #LCD
        self.lcd = lcddriver.lcd()

        self.lcd.lcd_clear()
        self.music_controler = mu.music_control()
        sleep(1)
        sleep(.25)
        self.lcd.lcd_display_string("Getting Things", 1)
        self.lcd.lcd_display_string("Ready", 2)

        self.radios_genres = {}

        self.radios_for_current_genre = None


        #rotations
        #--------------------------------------
        #self.globalcounter = 0
        #self.flag = 0
        #self.last_rob_status = 0
        #self.current_rob_status = 0
        #self.last_global_counter = 0
        #---------------------------------------

        # rotation device
        self.roAin = 17     
        self.roBin = 4
        self.roSin = 27
        # Options Selections
        #self.list_genre = self.music_controler.genres
        #self.current_genre = None # This will be used for just playing a different genre of music
        self.option_list = ["Mood Music", "Music Genre", "Play Genre", "Chosen Options"]
        #---------------------------------
        #for the genre and mood
        self.genre = None

        self.music_genres = []
        self.sub_music_genres = []


        self.mood = None
        #for the buttons
        self.btn_vermelho = 23
        self.btn_verde = 24
        self.btn_branco_esquerda = 25
        self.btn_branc_direita = 12

        #For the Bitalino Device
        self.bit_macAddress = "20:18:06:13:02:19"

        self.process = None         #for the multiprocess

        self.lcd.lcd_clear()

        with open("moods.txt", "r") as file:
            for i in file:
                a = i.split(",")
                self.radios_genres[a[0]] = {
                        "estado" : a[0],
                        "genero" : a[1][:len(a[1]) - 1],
                        "radios" : self.music_controler.get_genre_radios(a[1][:len(a[1]) - 1])
                }
                

        for keys,values in self.music_controler.json_genres.items():
            self.music_genres.append(keys)

        self.radios_genres["custom"] = {
            "estado" : "Unknown",
            "genero" : "Unknown",
            "radios" : "Unknown"
        }





    def setup(self):
        GPIO.setup(self.roAin, GPIO.IN)
        GPIO.setup(self.roBin, GPIO.IN)
        GPIO.setup(self.roSin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.setup(self.btn_vermelho, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn_verde, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn_branco_esquerda, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn_branc_direita, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def main(self):
        self.lcd.lcd_display_string('Welcome to',1)
        self.lcd.lcd_display_string('MoodShifter!', 2)
        sleep(3)
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string('Please Select',1)
        self.lcd.lcd_display_string('An Option', 2)
        sleep(4)
        self.main_menu()

    
    def main_menu(self):
            
        last_rob_status = 0
        current_rob_status = 0
        flag = 0
        globalcounter = 0
        last_global_counter = 0
        acept = None

        self.lcd.lcd_clear()
        sleep(.25)
        self.lcd.lcd_display_string("Main Menu", 1)
        self.lcd.lcd_display_string(self.option_list[globalcounter], 2)
        while acept != "yes":
            if not (GPIO.input(self.btn_verde)):
                acept = "yes"

            if not (GPIO.input(self.btn_vermelho)):
                tempo_espera = time() + 3
                while(not (GPIO.input(self.btn_vermelho))):
                    if (tempo_espera < time()):
                        sleep(.5)
                        self.change_options()
                        #print("Done")

            
            last_rob_status = GPIO.input(self.roBin)
            while(not GPIO.input(self.roAin)):
                current_rob_status = GPIO.input(self.roBin)
                flag = 1
            if flag == 1:
                flag = 0
                if (last_rob_status == 0) and (current_rob_status == 1) and (globalcounter != 0):
                    globalcounter = globalcounter - 1
                if (last_rob_status == 1) and (current_rob_status == 0) and globalcounter < len(self.option_list) - 1:
                    globalcounter = globalcounter + 1
                if last_global_counter != globalcounter:
                    last_global_counter = globalcounter
                    self.lcd.lcd_clear()
                    self.lcd.lcd_display_string("Main Menu", 1)
                    self.lcd.lcd_display_string(self.option_list[globalcounter], 2)
        

        if self.option_list[globalcounter] == self.option_list[0]: #CASE for mood check
            self.current_mood_view()
        elif self.option_list[globalcounter] == self.option_list[1]: #CASE for music genre
            self.genre_options()
        elif self.option_list[globalcounter] == self.option_list[2]: # CASE play music 
            self.play_music_menu()
        elif self.option_list[globalcounter] == self.option_list[3]: # CASE CHOSEN OPTIONS
            self.chosen_options()





    def current_mood_view(self):
        print("entrei aqui no mood")
        self.mood = None
        bit_device = None

        self.lcd.lcd_clear()
        sleep(.25)
        #while bit_device == None:
        try:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("Trying to Connect", 1)
            self.lcd.lcd_display_string("To Bitalino", 2)
            bit_device = BITalino(self.bit_macAddress)
        except:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("Problem Found",1 )
            self.lcd.lcd_display_string("While Connecting", 2)
            sleep(2)
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("Please Check", 1)
            self.lcd.lcd_display_string("Bitalino", 2)
            sleep(5)
            self.main_menu()

        self.lcd.lcd_display_string(bit_device.version(), 1)
        sleep(3)
        self.main_menu()





    def genre_options(self):
        last_rob_status = 0
        current_rob_status = 0
        flag = 0
        globalcounter = 0
        last_global_counter = 0
        time_limit = time() + 60

        cancel = None
        acept = None

        self.genre = None

        self.lcd.lcd_clear()
        sleep(.25)
        self.lcd.lcd_display_string(self.option_list[1], 1)


        self.lcd.lcd_display_string(self.music_genres[globalcounter], 2)
        while time_limit > time():
            if not (GPIO.input(self.btn_verde)):
                acept = "yes"
            if not(GPIO.input(self.btn_vermelho)):
                cancel = "yes"
            
            if acept == "yes" or cancel == "yes":
                break
            
            last_rob_status = GPIO.input(self.roBin)
            while(not GPIO.input(self.roAin)):
                current_rob_status = GPIO.input(self.roBin)
                flag = 1
             
            if flag == 1:
                flag = 0
                if (last_rob_status == 0) and (current_rob_status == 1) and (globalcounter != 0):
                    globalcounter = globalcounter - 1
                if (last_rob_status == 1) and (current_rob_status == 0) and globalcounter < len(self.music_genres) - 1:
                    globalcounter = globalcounter + 1
                if last_global_counter != globalcounter:
                    
                    last_global_counter = globalcounter
                    time_limit = time() + 60
                    self.lcd.lcd_clear()
                    self.lcd.lcd_display_string(self.option_list[1], 1)

                    #if len(self.list_genre[globalcounter][1]) <= 16 :
                    #self.long_string(self.lcd,self.list_genre[globalcounter][1], 2, 16)
                    
                    #else:
                    #    self.process = multiprocessing.Process(target=self.long_string, args=(self.lcd,self.list_genre[globalcounter][1],2,16,))
                    #    self.process.start()

                    self.lcd.lcd_display_string(self.music_genres[globalcounter], 2)
        
        if cancel == "yes" or time() > time_limit:
            self.main_menu()

        elif acept == "yes":
            #self.genre = self.list_genre[globalcounter][1]
            #self.lcd.lcd_clear()
            #self.lcd.lcd_display_string('Getting Radios', 1)
            #self.lcd.lcd_display_string('For {0}'.format(self.music_genres[globalcounter][1]), 2)
            #self.music_controler.get_genre_radios(self.music_genres[globalcounter][0])
            #self.main_menu()
            sleep(0.25)
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("Choose SubGenre", 1)

            genres_to_check = self.music_controler.json_genres[self.music_genres[globalcounter]]
            self.lcd.lcd_display_string(genres_to_check[globalcounter], 2)

            last_rob_status = 0
            current_rob_status = 0
            flag = 0
            globalcounter = 0
            last_global_counter = 0
            time_limit = time() + 60

            cancel = None
            acept = None
            
            while time_limit > time():
                if not (GPIO.input(self.btn_verde)):
                    acept = "yes"
                if not(GPIO.input(self.btn_vermelho)):
                    cancel = "yes"
            
                if acept == "yes" or cancel == "yes":
                    break
            
                last_rob_status = GPIO.input(self.roBin)
                while(not GPIO.input(self.roAin)):
                    current_rob_status = GPIO.input(self.roBin)
                    flag = 1
             
                if flag == 1:
                    flag = 0
                    if (last_rob_status == 0) and (current_rob_status == 1) and (globalcounter != 0):
                        globalcounter = globalcounter - 1
                    if (last_rob_status == 1) and (current_rob_status == 0) and globalcounter < len(genres_to_check) - 1:
                        globalcounter = globalcounter + 1
                    
                    if last_global_counter != globalcounter:
                    
                        last_global_counter = globalcounter
                        time_limit = time() + 60
                        self.lcd.lcd_clear()
                        self.lcd.lcd_display_string("Choose SubGenre", 1)

                        self.lcd.lcd_display_string(genres_to_check[globalcounter], 2)
        
            if cancel == "yes" or time() > time_limit:
                self.self.genre_options()
        

            elif acept == "yes":
                self.genre = genres_to_check[globalcounter]
                self.lcd.lcd_clear()
                self.lcd.lcd_display_string('Getting Radios', 1)
                self.lcd.lcd_display_string('For {0}'.format(self.genre), 2)
                self.radios_genres["custom"]["genero"] = self.genre
                self.radios_genres["custom"]["radios"] = self.music_controler.get_genre_radios(self.genre)

                #self.radios_for_current_genre = self.music_controler.get_genre_radios(self.genre)
                self.main_menu()


    def play_music_menu(self):
        globalcounter = 0
        last_global_counter = 0

        current_radio = 0

        radio_pid = None

        #if self.mood == None:
        #    time_limit = time() + 60
            # self.lcd.lcd_clear()
            # self.lcd.lcd_display_string('Your mood is', 1)
            # self.lcd.lcd_display_string('Still Unknown', 2)
            # sleep(2)
            # self.lcd.lcd_clear()
            # self.lcd.lcd_display_string('Would you like', 1)
            # self.lcd.lcd_display_string('to check it now?', 2)
            # sleep(2)
            # self.lcd.lcd_clear()
            # self.lcd.lcd_display_string('Green for Yes', 1)
            # self.lcd.lcd_display_string('Red for No', 2)
            
            # acept = None
            # cancel = None
            
            # while time_limit > time():
            #     if not (GPIO.input(self.btn_verde)):
            #         acept = "yes"
            #     if not(GPIO.input(self.btn_vermelho)):
            #         cancel = "yes"
            #     if acept == "yes" or cancel == "yes":
            #         break
            # if acept == "yes":
            #     self.current_mood_view()
            # elif time() > time_limit:
            #     self.main_menu()

            # elif cancel == "yes":
            #     sleep(.25)
            #     pass
        
        if self.genre == None:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string('No Genre Chosen!', 1)
            self.lcd.lcd_display_string('Select a Genre', 2)
            sleep(3)
            self.genre_options()

        #PARA EFEITOS DE PROTOTIPO, MUDAR DEPOIS
        #start first radio play
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string('Please Select', 1)
        self.lcd.lcd_display_string('Mood to Play', 2)
        sleep(3)
        
        blah = []
        for keys,items in self.radios_genres.items():
            blah.append(keys)

        self.lcd.lcd_clear()
        self.lcd.lcd_display_string('Choose Mood', 1)
        self.lcd.lcd_display_string(blah[globalcounter], 2)

        
        while True:
            if not(GPIO.input(self.btn_vermelho)):
                sleep(.25)
                self.main_menu()

            if not(GPIO.input(self.btn_branco_esquerda)):
                if globalcounter != 0:
                    globalcounter = globalcounter - 1
                    sleep(.25)

            if not(GPIO.input(self.btn_branc_direita)):
                if globalcounter < len(blah) - 1:
                    globalcounter = globalcounter + 1
                    sleep(.25)

            if not (GPIO.input(self.btn_verde)):
                break
            
            if globalcounter != last_global_counter:
                #self.killProcess()
                last_global_counter = globalcounter
                #os.kill(os.getpgid(radio_pid.pid), signal.SIGTERM)
                self.lcd.lcd_clear()
                self.lcd.lcd_display_string('Choose Mood', 1)
                self.lcd.lcd_display_string(blah[globalcounter], 2)

        self.lcd.lcd_clear()
        self.lcd.lcd_display_string('Playing Radio', 1)
        

        if len(self.radios_genres[blah[globalcounter]]["radios"][current_radio][0]) <= 16 :
            self.long_string(self.lcd,self.radios_genres[blah[globalcounter]]["radios"][current_radio][0], 2, 16)
        else:
            self.process = multiprocessing.Process(target=self.long_string, args=(self.lcd,self.radios_genres[blah[globalcounter]]["radios"][current_radio][0],2,16,))
            self.process.start()
        #self.lcd.lcd_display_string('{0}'.format(self.music_controler.genre_radios[last_global_counter][0]), 2)
        radio_pid = subprocess.Popen(["mplayer","-playlist", self.radios_genres[blah[globalcounter]]["radios"][current_radio][1]], preexec_fn=os.setsid)
        #_---------------------------------------------------------
        
        globalcounter = 0
        last_global_counter = 0

        while True:
            if not(GPIO.input(self.btn_vermelho)):
                os.kill(os.getpgid(radio_pid.pid), signal.SIGTERM)
                self.killProcess()
                sleep(.25)
                break

            if not(GPIO.input(self.btn_branco_esquerda)):
                if globalcounter != 0:
                    globalcounter = globalcounter - 1
                    sleep(.25)

            if not(GPIO.input(self.btn_branc_direita)):
                if globalcounter < len(self.radios_genres[blah[globalcounter]]["radios"]) - 1:
                    globalcounter = globalcounter + 1
                    sleep(.25)
            
            if globalcounter != last_global_counter:
                
                self.killProcess()
                last_global_counter = globalcounter
                os.kill(os.getpgid(radio_pid.pid), signal.SIGTERM)
                self.lcd.lcd_clear()
                self.lcd.lcd_display_string('Playing Radio:', 1)
                if len(self.radios_genres[blah[globalcounter]]["radios"][last_global_counter][0]) <= 16 :
                    self.long_string(self.lcd,self.radios_genres[blah[globalcounter]]["radios"][last_global_counter][0], 2, 16)
                else:
                    self.process = multiprocessing.Process(target=self.long_string, args=(self.lcd,self.radios_genres[blah[globalcounter]]["radios"][last_global_counter][0],2,16,))
                    self.process.start()
                #self.long_string(self.lcd, self.music_controler.genre_radios[last_global_counter][0], 2)
                #self.lcd.lcd_display_string('{0}'.format(self.music_controler.genre_radios[last_global_counter][0]))
                radio_pid = subprocess.Popen(["mplayer","-playlist", self.radios_genres[blah[globalcounter]]["radios"][last_global_counter][1]], preexec_fn=os.setsid)

        self.main_menu()


    def change_options(self):
        self.lcd.lcd_clear()
        self.killProcess()
        globalcounter = 0

        while True:
            if not(GPIO.input(self.btn_vermelho)):
                os.kill(os.getpgid(radio_pid.pid), signal.SIGTERM)
                self.killProcess()
                sleep(.25)
                break

            if not(GPIO.input(self.btn_branco_esquerda)):
                if globalcounter != 0:
                    globalcounter = globalcounter - 1
                    sleep(.25)

            if not(GPIO.input(self.btn_branc_direita)):
                if globalcounter <  3:
                    globalcounter = globalcounter + 1
                    sleep(.25)
            
            if globalcounter != last_global_counter:
                self.killProcess()
                self.process = multiprocessing.Process(target=self.long_string, args=(self.lcd,self.music_controler.genre_radios[last_global_counter][0],2,16,))
                self.process.start()
                
                
                

        self.main_menu()

        



    def chosen_options(self):

        globalcounter = 0
        last_global_counter = 0
        time_limit = time() + 60

        cancel = None

        blah = []
        for keys,items in self.radios_genres.items():
            blah.append(keys)

        print(blah)

        
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("Mood:", 1)
        self.lcd.lcd_display_string("{0}".format(self.radios_genres[blah[globalcounter]]["genero"]), 2)

        sleep(.25)
        while time_limit > time():
            if not(GPIO.input(self.btn_vermelho)):
                cancel = "yes"
            
            if not(GPIO.input(self.btn_branco_esquerda)):
                if globalcounter != 0:
                    globalcounter = globalcounter - 1
                    time_limit = time() + 60

            if not(GPIO.input(self.btn_branc_direita)):
                if globalcounter < len(blah) - 1:
                    globalcounter = globalcounter + 1
                    time_limit = time() + 60
                    
            if cancel == "yes":
                break

            if globalcounter != last_global_counter:
                last_global_counter = globalcounter
                self.lcd.lcd_clear()
                self.lcd.lcd_display_string("Mood:", 1)
                self.lcd.lcd_display_string("{0}".format(self.radios_genres[blah[globalcounter]]["genero"]), 2)

        self.main_menu()

    def long_string(self, display, text='', num_line=1, num_cols=16):
        """
        Parameters: (driver, string to print, number of line to print, number of columns of your display)
        Return: This function send to display your scrolling string.
        """
        if (len(text) > num_cols):
            while True:
                display.lcd_display_string(text[:num_cols], num_line)
                sleep(.5)
                for i in range(len(text) - num_cols + 1):
                    text_to_print = text[i:i + num_cols]
                    display.lcd_display_string(text_to_print, num_line)
                    sleep(0.2)
                sleep(1)
        else:
            display.lcd_display_string(text, num_line)

    def destroy(self):
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("GOOD BYE LAD", 1)
        self.lcd.lcd_display_string("GET WELL SOON", 2)
        sleep(4)
        self.lcd.lcd_clear()

        GPIO.cleanup()

    def killProcess(self):
        if self.process is not None:
            try:

                self.process.terminate()
                self.process = None
            except:
                pass

if __name__=='__main__':
    programa = program()
    programa.setup()
    try:
        programa.main()
    except KeyboardInterrupt:
        programa.destroy()
