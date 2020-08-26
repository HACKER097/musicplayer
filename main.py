import curses
from curses import textpad
import os
import pygame

os.system('ls ~/Music >> names.txt')
names = open("names.txt", 'r+')
menu = names.readlines(1000000)
names.truncate(0)



def play(current):
	playing = current
	pygame.mixer.quit()
	pygame.mixer.init(frequency=48000)
	pygame.mixer.music.load(menu[current].replace('\n',''))
	pygame.mixer.music.play()

def main(stdscr):

	curses.curs_set(0)
	pygame.mixer.init(frequency=48000)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	current = 2
	down_limit = 23
	up_limit = 0
	pause = False

	while True:
		playing = 0
		stdscr.refresh()
		key = stdscr.getch()
		h, w = stdscr.getmaxyx()
		y = h//2 - len(menu)//2
		x = w - 4*w//5
		
		box = [[3,26], [h-5, w-10]]
		

		if key == curses.KEY_UP and current > 0:
			current-=1
			down_limit-=1
			up_limit-=1
			stdscr.clear()

		if key == curses.KEY_DOWN and current < len(menu)-1:
			current+=1
			down_limit+=1
			up_limit+=1
			stdscr.clear()

		if key == curses.KEY_ENTER or key == 10 or key == 13:
			play(current)

		if key == ord(' '):
			if pause == True:
				pygame.mixer.music.unpause()
				pause = False
			elif pause == False:
				pygame.mixer.music.pause()
				pause = True

		for i in range(len(menu)):
			if i < down_limit and i > up_limit:
				if current == i:
					stdscr.attron(curses.color_pair(1))
					stdscr.addstr(y+i-down_limit+45, x, menu[i])
					stdscr.attroff(curses.color_pair(1))
				elif playing == i:
					stdscr.attron(curses.color_pair(2))
					stdscr.addstr(y+i-down_limit+45, x, menu[i])
					stdscr.attroff(curses.color_pair(2))
				else:	
					stdscr.addstr(y+i-down_limit+45, x, menu[i])
			stdscr.refresh()
		textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1],)
		stdscr.addstr(26, x, str(pygame.mixer.music.get_pos()))		


		



curses.wrapper(main)
