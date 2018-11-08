from time import sleep, time
from Adafruit_CharLCD import Adafruit_CharLCD as adafruit
import RPi.GPIO as GPIO
import music as mu
import subprocess, os, signal


"""
TODO:
	1  fazer menu para o bitalino
"""


class program:
	def __init__(self):
		#LCD
		self.lcd = adafruit (rs = 26, en=19, d4 = 13, d5 = 6, d6 = 5, d7 = 11, cols= 16, lines = 2)

		self.lcd.clear()
		self.lcd.message('Preparing System\nStandby Please')
		sleep(1)

		self.music_controler = mu.music_control()

		self.lcd.clear()

		#rotations
		#--------------------------------------
		self.globalcounter = 0
		self.flag = 0
		self.last_rob_status = 0
		self.current_rob_status = 0
		self.last_global_counter = 0
		#---------------------------------------

		#rotation device
		self.roAin = 17		
		self.roBin = 18
		self.roSin = 27
		#self.list_genre = ["Alternative" ,"Blues" ,"Classical", "Country" ,"Dance",
 		#		"Easy Listening" , "Electronic" , "European", "Hip Hop",
 		#		"Indie Pop", "Inspirational", "Asian Pop", "Jazz", "Latin",
 		#		"New Age", "Opera", "Pop", "R&B / Soul", "Reggae", "Rock",
		#		"Singer", "World Music"]
		self.list_genre = self.music_controler.genres
		
		self.option_list = ["Check Mood", "Music Genre", "Play Music", "Chosen Options"]

		self.selected_option = None
		#---------------------------------
		#for the genre and mood
		self.genre = None
		self.mood = None
		#for the buttons
		self.btn_vermelho = 23
		self.btn_verde = 24
		self.btn_branco_esquerda = 25
		self.btn_branc_direita = 12



	def setup(self):
		GPIO.setup(self.roAin, GPIO.IN)
		GPIO.setup(self.roBin, GPIO.IN)
		GPIO.setup(self.roSin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		GPIO.setup(self.btn_vermelho, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.btn_verde, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.btn_branco_esquerda, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.btn_branc_direita, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	def main(self):
		self.lcd.message('Welcome to\nMoodShifter!')
		sleep(3)
		self.lcd.clear()
		self.lcd.message('Please Select\nAn Option')
		sleep(4)
		self.main_menu()

	
	def main_menu(self):
		def acept_event():
			return "yes"
			
		last_rob_status = 0
		current_rob_status = 0
		flag = 0
		globalcounter = 0
		last_global_counter = 0
		acept = None

		self.lcd.clear()
		sleep(.25)
		self.lcd.message("Main Menu" + '\n' + self.option_list[globalcounter])
		while acept != "yes":
			if not (GPIO.input(self.btn_verde)):
				acept = acept_event()
			
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
			 		self.lcd.clear()
			 		self.lcd.message("Main Menu\n" + self.option_list[globalcounter])
		

		if self.option_list[globalcounter] == self.option_list[0]: #CASE for mood check
			self.current_mood_view()
		elif self.option_list[globalcounter] == self.option_list[1]: #CASE for music genre
			self.genre_options()
		elif self.option_list[globalcounter] == self.option_list[2]: # CASE play music 
			self.play_music_menu()
		elif self.option_list[globalcounter] == self.option_list[3]: # CASE CHOSEN OPTIONS
			self.chosen_options()





	def current_mood_view(self):
		print("im in the current_mood_view")


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

		self.lcd.clear()
		sleep(.25)
		self.lcd.message(self.option_list[1] + '\n' + self.list_genre[globalcounter][1])
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
			 	if (last_rob_status == 1) and (current_rob_status == 0) and globalcounter < len(self.list_genre) - 1:
			 		globalcounter = globalcounter + 1
			 	if last_global_counter != globalcounter:
			 		last_global_counter = globalcounter
			 		time_limit = time() + 60
			 		self.lcd.clear()
			 		self.lcd.message(self.option_list[1] + '\n' + self.list_genre[globalcounter][1])
		
		if cancel == "yes" or time() > time_limit:
			self.main_menu()
		

		elif acept == "yes":
			self.genre = self.list_genre[globalcounter][1]
			self.lcd.clear()
			self.lcd.message('Getting Radios\nFor {0}'.format(self.list_genre[globalcounter][1]))
			self.music_controler.get_genre_radios(self.list_genre[globalcounter][0])
			self.main_menu()


	def play_music_menu(self):
		globalcounter = 0
		last_global_counter = 0

		radio_pid = None

		if self.mood == None:
			time_limit = time() + 60
			self.lcd.clear()
			self.lcd.message('Your mood is\nStill Unknown')
			sleep(2)
			self.lcd.clear()
			self.lcd.message('Would you like\nto check it now?')
			sleep(2)
			self.lcd.clear()
			self.lcd.message('Green for Yes\nRed for No')
			
			acept = None
			cancel = None
			
			while time_limit > time():
				if not (GPIO.input(self.btn_verde)):
					acept = "yes"
				if not(GPIO.input(self.btn_vermelho)):
					cancel = "yes"
				if acept == "yes" or cancel == "yes":
					break
			if acept == "yes":
				self.current_mood_view()
			elif time() > time_limit:
				self.main_menu()

			elif cancel == "yes":
				sleep(.25)
				pass
		
		if self.genre == None:
			self.lcd.clear()
			self.lcd.message('No Genre Chosen!\nSelect a Genre')
			sleep(3)
			self.genre_options()

		#start first radio play
		self.lcd.clear()
		self.lcd.message('Playing Radio\n{0}'.format(self.music_controler.genre_radios[last_global_counter][0]))
		radio_pid = subprocess.Popen(["mplayer","-playlist", self.music_controler.genre_radios[last_global_counter][1]], preexec_fn=os.setsid)
		#_---------------------------------------------------------
		while True:
			if not(GPIO.input(self.btn_vermelho)):
				os.kill(os.getpgid(radio_pid.pid), signal.SIGTERM)
				sleep(.25)
				break

			if not(GPIO.input(self.btn_branco_esquerda)):
				if globalcounter != 0:
					globalcounter = globalcounter - 1
					sleep(.25)

			if not(GPIO.input(self.btn_branc_direita)):
				if globalcounter != len(self.music_controler.genre_radios):
					globalcounter = globalcounter + 1
					sleep(.25)
			
			if globalcounter != last_global_counter:
				last_global_counter = globalcounter
				os.kill(os.getpgid(radio_pid.pid), signal.SIGTERM)
				self.lcd.clear()
				self.lcd.message('Playing Radio\n{0}'.format(self.music_controler.genre_radios[last_global_counter][0]))
				radio_pid = subprocess.Popen(["mplayer","-playlist", self.music_controler.genre_radios[last_global_counter][1]], preexec_fn=os.setsid)

		self.main_menu()



	#FEITO

	def chosen_options(self):

		globalcounter = 0
		last_global_counter = 0
		time_limit = time() + 60

		cancel = None

		self.lcd.clear()
		sleep(.25)
		self.lcd.message("Current Mood:\n{0}".format(self.mood))
		while time_limit > time():
			if not(GPIO.input(self.btn_vermelho)):
				cancel = "yes"
			
			if not(GPIO.input(self.btn_branco_esquerda)):
				if globalcounter != 0:
					globalcounter = globalcounter - 1
					time_limit = time() + 60

			if not(GPIO.input(self.btn_branc_direita)):
				if globalcounter != 1:
					globalcounter = globalcounter + 1
					time_limit = time() + 60
					
			if cancel == "yes":
				break
			if globalcounter != last_global_counter:
				last_global_counter = globalcounter
				if globalcounter == 0:
					self.lcd.clear()
					self.lcd.message("Current Mood:\n{0}".format(self.mood))
				elif globalcounter == 1:
					self.lcd.clear()
					self.lcd.message("Genre Selected:\n{0}".format(self.genre))

		self.main_menu()







	def destroy(self):
		self.lcd.clear()
		self.lcd.message("GOOD BYE LAD\nGET WELL SOON")
		sleep(4)
		self.lcd.clear()

		GPIO.cleanup()

if __name__=='__main__':
	programa = program()
	programa.setup()
	try:
		programa.main()
	except KeyboardInterrupt:
		programa.destroy()




#BACKUPS
#----------------------------------------------------------------------------------------------------------------------------


#lcd.clear()

#lcd.message('Estado Actual:\n Deprimido xD')

#sleep(3)

#for x in range(0,16):
#	lcd.move_right()
#	sleep(.1)
#sleep(3)
#
#lcd.clear()
#
#lcd.message('fogo finalmente\n consegui!')
#
#sleep(3)
#
#for x in range(0, 16):
#	lcd.move_left()
#	sleep(.1)

#lcd.clear()

# def select_genre():
	# 	self.genre = None
	# 	GPIO.add_event_detect(self.btn_verde, GPIO.IN)
	# 	while self.genre == None:
	# 		self.last_rob_status = GPIO.input(self.roBin)
	# 		while(not GPIO.input(roAin)):
	# 			self.current_rob_status = GPIO.input(self.roBin)
	# 			self.flag = 1
	# 		if self.flag == 1:
	# 			self.flag = 0
	# 			if (self.last_rob_status == 0) and (self.current_rob_status == 1) and (self.globalcounter != 0):
	# 				self.globalcounter = globalcounter - 1
	# 			if (self.last_rob_status == 1) and (self.current_rob_status == 0) and self.globalcounter + 1 < len(self.list_genre):
	# 				self.globalcounter = self.globalcounter + 1
	# 			if self.last_global_counter != self.globalcounter:
	# 				self.last_global_counter = self.globalcounter
	# 				self.lcd.clear()
	# 				self.lcd.message('Music Genre:\n' + self.list_genre[self.globalcounter])

