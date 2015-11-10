import os 
import time
from Tkinter import *
from ttk import *
from tkFileDialog import askopenfilename, asksaveasfilename
from pydub import AudioSegment
import subprocess
from pydub.playback import play
import tkMessageBox

TEMP_FILE = "mashup.mp3"

class ApplicationUI(Frame):

	def __init__(self, master = None):
		master.minsize(width=350, height=200)
		master.maxsize(width=350, height=200)
		Frame.__init__(self, master)
		self.grid()
		self.pack()
		self.createWidgets()
		

	def createWidgets(self):

		self.title = Label(self, text="Music reverser!", font=("Helvetica", 16))
		self.title.grid(row=0, column=1, columnspan=2)

		self.open_file = Button(self)
		self.open_file['text'] = "OPEN"
		self.open_file["command"] = self.openfile
		self.open_file.grid(row=1, column=0)

		self.save_button = Button(self, text='SAVE',
									command=self.save_file)
		self.save_button.grid(row=1, column=3)

		self.status_label= Label(self, text="Initial state", font=("Helvetica", 14))
		self.status_label.grid(row=2, column=0, rowspan=2, columnspan=4)

		self.play_song_button= Button(self)
		self.play_song_button['text'] = "PLAY"
		self.play_song_button["command"] = self.play
		self.play_song_button.grid(row=5, column=1)

		self.stop_button = Button(self, text='STOP', command=self.stop_playing)
		self.stop_button.grid(row=5, column=2)
					
		self.reverse_button = Button(self, text="REVERSE", command=self.reverse_song)
		self.reverse_button.grid(row=6, column=1)

		self.quit_button = Button(self, text="QUIT", command=self.quit)
		self.quit_button.grid(row=6, column=3)

	def openfile(self):
		if hasattr(self, 'backwards'):
			del self.backwards
		self.filename = askopenfilename() 
		self.song = AudioSegment.from_mp3(self.filename)

	def play(self):
		if hasattr(self, 'player'):
			self.player.terminate()
		if hasattr(self, 'backwards'):
			self.play_reversed()
			self.status_label['text']="Playing reversed song"
		else:
			self.status_label['text']="Playing initial song"
		self.player = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", self.filename], 
									stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
									stderr=subprocess.PIPE)

	def quit(self):
		if hasattr(self, 'player'):
			self.player.terminate()
			os.remove(TEMP_FILE)
		root.destroy()

	def reverse_song(self):
		if hasattr(self, 'song'):
			self.backwards = self.song.reverse()
			with open(TEMP_FILE, 'wb') as f:
				self.backwards.export(f.name, format="mp3")
		else:
			tkMessageBox.showinfo('Warning', "Open the file to be reversed first")

	def save_file(self):
		if hasattr(self, 'backwards'):
			self.filename=asksaveasfilename()
			with open(self.filename, 'wb') as f:
				self.backwards.export(f.name, format="mp3")

	def play_reversed(self):
		if hasattr(self, 'backwards'):
			self.filename=TEMP_FILE
		else:
			tkMessageBox.showinfo("Warning", "You should reverse the file first")

	def stop_playing(self):
		if hasattr(self, 'player'):
			self.status_label['text'] = 'File stopped to play'
			self.player.terminate()
		else:
			tkMessageBox.showinfo("Warning", "No music is playing")
		

root = Tk()
app = ApplicationUI(master=root)
app.mainloop()
