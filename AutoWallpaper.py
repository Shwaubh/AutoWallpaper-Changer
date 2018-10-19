import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import datetime
import requests
import bs4
import random
import urllib.request as urr
import os

totalFiles = 0

def setAsWallPaper(data):
	os.system('gsettings set org.cinnamon.desktop.background picture-uri file://"'+data+'"')
		
def setPath():
	if isFirstTime() == 1:
		pass
	else:
		showCustomeErrorMessage('Set Path For Saving Images' , 'This Application might be reset or opened first time')

def getPath():
	f = open('autoWallData.txt' , 'r')
	return f.read()

def getHtml(query):
	xx = query.split(' ')
	query = '+'.join(xx)
	url_ = "https://www.bing.com/images/search?q="+query+"&go=Search&qs=ds&form=QBIR"
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	req = urr.Request(url_ , None , headers)
	r = urr.urlopen(req)
	return r.read()

def addFile(s , search_):
	if len(search_) == 0:
		return 'Error'
	try:
		global totalFiles
		totalFiles = 0
		f = open(s+'/index.txt' , 'w')
		data = getHtml(search_)
		soup = bs4.BeautifulSoup(data , 'html.parser')
		soup.prettify()
		images = soup.find_all('img',{'class' : 'mimg'})
		for i in images:
			if 'id' in i.attrs.keys():
				pass
			elif 'src' in i.attrs.keys():
				f.write(str(i.attrs['src'])+'\n')
				totalFiles+=1
			else:
				totalFiles+=1
				f.write(str(i.attrs['data-src'])+'\n')
		f.close()
		return 1
	except Exception as ee:
		return ee

def downloadThisPath():
	global totalFiles
	n = random.randint(1,totalFiles-1)
	f = open(getPath()+'/index.txt' , 'r')
	c = 0
	url_ = ''
	for i in f:
		url_ = str(i)
		c+=1
		if c == n:
			break
	f.close()
	r = requests.get(url_+'.jpg')
	with open(getPath()+'/one.jpg' , 'wb') as f:
		f.write(r.content)
	return getPath()+'/one.jpg'
		
def isFirstTime():
	try:
		f = open('autoWallData.txt' , 'r')
		return 1
	except FileNotFoundError:
		f = open('autoWallData.txt' , 'w')
		f.close()
		return 0

def showCustomeErrorMessage(title , message):
	if messagebox.showerror(title ,message) == 'ok':
		s = filedialog.askdirectory()
		f = open('autoWallData.txt' , 'w')
		f.write(s)
		f.close()
		
class MainFrame(Frame):
	def __init__(self , root):
		super().__init__(root)
		self.pack()
		self.createWidget()
		
	
	def showMessage(self):
		msg = addFile(getPath() , self.keyEntry.get())
		if msg == 1:
			data = downloadThisPath()
			setAsWallPaper(data)
		else:
			messagebox.showerror('Error Occurred' , msg)
		
	def createWidget(self):
		self.key = Label(self , text = 'Keyword')
		self.key.grid(row = 0 , column = 0 , padx = 20 , pady = 20)
		
		self.keyEntry = Entry(self)
		self.keyEntry.grid(row = 0 , column = 1 )
		
		self.set  = Button(self , text = 'Set' , command=self.showMessage)
		self.set.grid(row = 1 , column = 0 , columnspan = 2 )	
	
		
	def setTitle(self , title):
		self.master.title(title)
		
	def setSize(self , size):
		s = size.split('x')
		self.master.maxsize(int(s[0]) , int(s[1]))
		self.master.minsize(int(s[0]),int(s[1]))
		self.master.geometry(size)
		
		
root = Tk()
main = MainFrame(root)
main.setTitle('Saurabh')
main.setSize('300x100')
setPath()
path = getPath()
setAsWallPaper('/home/saurabhsk/Pictures/AutoWallPaper/one.jpg')
root.mainloop()
