from PIL import ImageTk, Image, ImageOps
import tkinter

import os 
import time
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import Button, Label, OptionMenu, Canvas, StringVar
import subprocess
import tkinter.messagebox

OPTIONS = ['gray', 'red', 'blue', ]

class ApplicationUI(tkinter.Frame):

	def __init__(self, master = None):
		master.minsize(width=550, height=450)
		master.maxsize(width=550, height=450)
		tkinter.Frame.__init__(self, master)
		self.grid()
		self.pack()
		self.createWidgets()
		

	def createWidgets(self):
		self.title = Label(self, text="Image!", font=("Helvetica", 16))
		self.title.grid(row=0, column=1, columnspan=2)

		self.open_file = Button(self)
		self.open_file['text'] = "OPEN"
		self.open_file["command"] = self.openfile
		self.open_file.grid(row=1, column=0)

		self.save_button = Button(self, text='SAVE',
									command=self.save_file)
		self.save_button.grid(row=1, column=1)

		self.canvas = Canvas(self, width=400, height=300)
		self.canvas.grid(row=2, column=0, rowspan=5, columnspan=4)

		self.convert_grayscale_button= Button(self)
		self.convert_grayscale_button['text'] = "Convert to\n grayscale"
		self.convert_grayscale_button["command"] = self.convert_grayscale
		self.convert_grayscale_button.grid(row=7, column=0)

		self.variable = StringVar(self)
		self.variable.set("gray") 
		self.choose_color_menu = OptionMenu(self, self.variable,"gray", "blue", "green", "red")
		self.choose_color_menu['text'] = "Choose Color"
		self.choose_color_menu.grid(row=7, column=1)
					
		self.color_button = Button(self, text="COLOR", command=self.color_image)
		self.color_button.grid(row=7, column=2)

		self.quit_button = Button(self, text="QUIT", command=self.quit)
		self.quit_button.grid(row=7, column=3)
	
	def openfile(self):
		self.filename = askopenfilename()
		self.pilImage = Image.open(self.filename)
		width, height = self.pilImage.size
		rate = 400/width
		new_width = 400
		new_height = int(height*rate)
		print (new_width, new_height)
		self.pilImage=self.pilImage.resize((new_width, new_height), Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(self.pilImage)
		self.canvas.create_image(250, 200, image=self.image, anchor='center')

	def save_file(self):
		self.filename=asksaveasfilename()
		with open(self.filename, 'wb') as f:
			self.backwards.export(f.name, format="png")

	def quit(self):
		if hasattr(self, 'player'):
			os.remove(TEMP_FILE)
		root.destroy()

	def choose_color(self):
		self.color = self.variable.get()


	def color_image(self):
		if hasattr(self, 'grayImage'):
			self.choose_color()
			if self.color == 'blue':
				color = '#0000FF'
			elif self.color == 'red':
				color = '#FF0000'
			elif self.color == 'green':
				color = '#00FF00'
			self.coloredImg = ImageOps.colorize(self.grayImage, (0,0,0,0), color)
			self.image = ImageTk.PhotoImage(self.coloredImg)
			self.canvas.create_image(250, 200, image=self.image, anchor='center')
		else:
			tkMessageBox.showinfo('Warning', "Convert the file to grayscale first")

	def convert_grayscale(self):
		self.grayImage = self.pilImage.convert('L')
		self.image = ImageTk.PhotoImage(self.grayImage)
		self.canvas.create_image(250, 200, image=self.image, anchor='center')


root = tkinter.Tk()
app = ApplicationUI(master=root)
app.mainloop()
