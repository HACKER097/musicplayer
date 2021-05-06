import curses
from curses import textpad
import time
import pathlib
from pathlib import Path
import vlc
import pafy
import os

def text_middle(stdscr, text, xoffset, yoffset, align = True):
	HIEGHT, WIDTH = 30, 110
	if align:
		stdscr.addstr(int(HIEGHT/2)+yoffset, int((WIDTH/2)-((len(str(text))/2)))+xoffset, text)
	else:
		stdscr.addstr(int(HIEGHT/2)+yoffset, int(WIDTH/2)+xoffset, text)

def print_list(stdscr, list, xoffset, yoffset, align = True):
	for i in range(len(list)):
		text_middle(stdscr, str(list[i]), xoffset, i+yoffset, align=align)

class banner:
	def __init__(self, stdscr, text, length, x, y, value):
		self.stdscr = stdscr
		self.text = text
		self.length = length
		self.x = x
		self.y = y
		self.value = value
		self.colorpairno = 1
		self.colorpairnochanger = 0

	def move(self):
		self.newtext = str(self.text)[:self.length+int(self.value)][int(self.value):]
		self.stdscr.attron(curses.color_pair(1))
		self.stdscr.addstr(self.y, self.x, self.newtext)
		self.stdscr.attroff(curses.color_pair(1))
		self.value+=0.2
		if self.value > len(str(self.text))-self.length:
			self.value = 0

	def blink(self):
		self.newtext = str(self.text)[:self.length+int(self.value)][int(self.value):]
		self.stdscr.attron(curses.color_pair(3))
		self.stdscr.addstr(self.y, self.x, self.newtext)
		self.stdscr.attroff(curses.color_pair(3))
		self.value+=0.2
		if self.value > len(str(self.text))-self.length:
			self.value = 0

class scroll_list:
	def __init__(self, stdscr, items, length, x, y, current):
		self.stdscr = stdscr
		self.items = items
		self.length = length
		self.x = x
		self.y = y
		self.current = current

	def scroll(self):
		self.stdscr.attron(curses.color_pair(6))
		if self.current >= self.length:
			self.newitems=self.items[self.current:][:self.length+(self.length-self.current)]
		else:
			self.newitems=self.items[:self.length]
		for i in range(len(self.newitems)):
			if i == self.current:
				if self.current >= self.length:
					self.current_banner = banner(self.stdscr, self.newitems[i-self.current], 30, self.x, self.y+i-self.current, 0)
				else:
					self.current_banner = banner(self.stdscr, self.newitems[i], 30, self.x, self.y+i, 0)
			else:
				self.stdscr.addstr(self.y+i, self.x, str(self.newitems[i])[:30])
		self.stdscr.attroff(curses.color_pair(6))



class window:
	def __init__(self, maxh, maxl):
		self.maxh = maxh
		self.maxl = maxl
		self.stdscr = curses.initscr()
		self.run = True
		self.path = path = Path('/home/hacker097/Downloads/twenty one pilots/')
		self.album_paths = [x for x in self.path.iterdir() if x.is_dir()]
		self.album_names = []
		for i in range(len(self.album_paths)):
			self.album_names.append(self.album_paths[i].stem)
		self.track_names=["Select a track"]
		self.track_paths=["Track name / Song name"]
		self.trackblink = False
		self.youtube_mode = False

	def play(self):
		try:		
			self.p.stop()
		except AttributeError:
			pass
		self.p = vlc.MediaPlayer(str(self.track_paths[self.tracklist.current]))
		self.p.play()
		self.track_banner = banner(self.stdscr, str(self.track_paths[self.tracklist.current]), 30, 55, 0, 0)
		self.playing_banner = banner(self.stdscr, "Playing: " + str(self.track_paths[self.tracklist.current].stem), 28, 1, 29, 0)


	def key_events(self):
		self.key = self.stdscr.getch()

		if self.key == curses.KEY_UP:
			self.currentlist.current-=1

		if self.key == curses.KEY_DOWN:
			self.currentlist.current+=1

		if self.currentlist.current < 0:
			self.currentlist.current = 0
		if self.currentlist.current > len(self.currentlist.items):
			self.currentlist.current = len(self.currentlist.items)

		if self.key == curses.KEY_RIGHT:
			self.currentlist = self.tracklist
		if self.key == curses.KEY_LEFT:
			self.currentlist = self.albumlist

		if self.currentlist == self.tracklist:
			trackblink = True

		if self.key == curses.KEY_ENTER or self.key == 10 or self.key == 13:
			if self.currentlist == self.albumlist:
				self.tracklist.current=0
				self.track_path = Path('/home/hacker097/Downloads/twenty one pilots/'+self.album_names[self.albumlist.current])
				self.track_paths = [p for p in self.track_path.iterdir() if p.is_file()]
				self.track_names.clear()
				for i in range(len(self.track_paths)):
					self.track_names.append(self.track_paths[i].stem)

			if self.currentlist == self.tracklist:
				self.play()

		if self.key == ord(" ") or self.key == ord("k"):
			try:
				self.p.pause()
			except AttributeError:
				pass

		if self.key == ord("l"):
			try:
				self.p.set_time(self.p.get_time()+5000)
			except AttributeError:
				pass
		
		if self.key == ord("j"):
			try:
				self.p.set_time(self.p.get_time()-5000)
			except AttributeError:
				pass

		if self.key == ord("s"):
			self.youtube_mode = True 

	def display(self):
		self.stdscr.erase()
		
		self.stdscr.attron(curses.color_pair(4))
		curses.textpad.rectangle(self.stdscr, 0, 30, 28, 110)
		curses.textpad.rectangle(self.stdscr, 0, 0, 28, 29)
		self.stdscr.attroff(curses.color_pair(4))
		self.albumlist.scroll()
		self.albumlist.current_banner.move()
		self.tracklist.scroll()
		if self.currentlist == self.tracklist:
			self.tracklist.current_banner.blink()
		else:
			self.tracklist.current_banner.move()

		if self.currentlist == self.albumlist:
			self.albumlist.current_banner.blink()
		else:
			self.albumlist.current_banner.move()

		try:
			self.ms = self.p.get_time()
			self.seconds=int((self.ms/1000)%60)
			self.minutes=int((self.ms/(1000*60))%60)
			if self.seconds < 10:
				self.seconds = "0"+str(self.seconds)
			if self.minutes < 10:
				self.minutes = "0"+str(self.minutes)

			self.time = str(self.minutes)+":"+str(self.seconds)
			self.stdscr.attron(curses.color_pair(2))
			self.stdscr.addstr(29,35 ,str(self.time))
			self.stdscr.attroff(curses.color_pair(2))
			self.stdscr.attron(curses.color_pair(1))
			self.stdscr.addstr(29,40 ,"[")
			self.stdscr.addstr(29,110 ,"]")
			self.bar_length = int(self.p.get_position()*69)
			for i in range(self.bar_length):
				self.stdscr.addstr(29, 41+i, "=")
			if not self.p.get_position() == 1:
				pass
				self.stdscr.addstr(29, 41+self.bar_length, "O")

			if self.p.is_playing():
				self.stdscr.addstr(29, 31 ,"[>]")
			else:
				self.stdscr.addstr(29, 31 ,"[//]")
			self.stdscr.attroff(curses.color_pair(1))

			self.track_banner.blink()
			self.album_banner.blink()
			self.playing_banner.blink()

			if self.youtube_mode:
				curses.echo()
				curses.nocbreak()
				self.stdscr.nodelay(False)
				self.stdscr.keypad(False)
				curses.curs_set(1)


				self.stdscr.addstr(27,31,"Enter YouTube url: ")
				self.youtube_url = self.stdscr.getstr()
				self.stdscr.addstr(25,31,self.youtube_url)

				try:
					self.p.stop()
					self.youtube_data = pafy.new(str(self.youtube_url))
					self.audio_url = self.youtube_data.getbestaudio()
					self.p = vlc.MediaPlayer(self.audio_url.url)
					self.p.play() 
					self.audio_title = self.youtube_data.title

					self.track_banner = banner(self.stdscr, str(self.audio_url), 30, 55, 0, 0)
					self.playing_banner = banner(self.stdscr, "Playing: " + self.audio_title, 28, 1, 29, 0)
				except ValueError:
					pass



				curses.noecho()
				curses.cbreak()
				self.stdscr.nodelay(True)
				self.stdscr.keypad(True)
				curses.curs_set(0)
				self.youtube_mode = False

		except AttributeError:
			pass


		self.stdscr.refresh()
		



	def main(self):
		self.stdscr.nodelay(True)
		self.stdscr.keypad(True)
		curses.curs_set(0)
		curses.start_color()
		curses.noecho()
		curses.cbreak()

		self.albumlist = scroll_list(self.stdscr, self.album_names, 26, 1, 2, 0)
		self.tracklist = scroll_list(self.stdscr, self.track_names, 50, 31, 2, 0)
		self.currentlist = self.albumlist
		self.album_banner = banner(self.stdscr, "Album name / Folder name", 10, 10, 0, 0)


		try:
			curses.init_pair(1, 226, 0) #passive selected text inner, outer
			curses.init_pair(2, 51, 0)  #timer color inner, outer
			curses.init_pair(3, 226, 6) #active selected inner, outer
			curses.init_pair(4, 51, 0)  #border coloer inner,outer
			curses.init_pair(6, 228, 0)  #regular text inner, outer
			'''

			curses.init_pair(1, 226, 0) #passive selected text inner, outer
			curses.init_pair(2, 51, 0)  #timer color inner, outer
			curses.init_pair(3, 226, 6) #active selected inner, outer
			curses.init_pair(4, 51, 0)  #border coloer inner,outer
			curses.init_pair(6, 228, 0)  #regular text inner, outer

			Colors:
			0 - black
			1 - red
			2 - green
			3 - brown
			4 - blue
			5 - purpe
			6 - cyan
			7 - gray
			8 - dark gray
			9 - pink
			10- bright green
			11- bright yellow
			12- bule 2
			13- purple 2
			14- cyan brighter
			15- bright white
			16- black 2

			https://en.wikipedia.org/wiki/ANSI_escape_code
			
			these are 8 bit colors, there are a total of 256 colors, use the link and scroll to 8 bit color section to see all colors

			also use curses.COLOR_<color name>


			'''

			self.test = scroll_list(self.stdscr, ["hello","traing","thing"], 3, 10, 10, 0)
			while self.run:
				self.HEIGHT, self.WIDTH = self.stdscr.getmaxyx()
				if self.HEIGHT < 30 or self.WIDTH < 110:
					print("Minnimum terminal size : 30x110")
					time.sleep(2)
					self.run = False
				else:
					self.key_events()
					self.display()
					time.sleep(0.05)


		finally:
			curses.echo()
			curses.nocbreak()
			curses.curs_set(1)
			self.stdscr.keypad(False)
			self.stdscr.nodelay(False)
			curses.endwin()


		curses.echo()
		curses.nocbreak()
		self.stdscr.keypad(False)
		self.stdscr.nodelay(False)
		curses.endwin()




main_window = window(30, 110)
main_window.main()


