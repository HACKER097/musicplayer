import os
from termcolor import colored
import readchar
import pygame
import multiprocessing
os.system('clear')
os.system('ls ~/Music >> names.txt')
names = open("names.txt", 'r+')
songs = names.readlines(10000000)
names.truncate(0)
exit = False
current = 0
selection = 0
playing= 0
pause=False
time = False

pygame.init()

def play(current):
	global playing
	playing = current
	pygame.mixer.quit()
	pygame.mixer.init(frequency=48000)
	pygame.mixer.music.load(songs[current].replace('\n',''))
	pygame.mixer.music.play()


def stop():
	global pause
	if pause == False:
		pygame.mixer.music.pause()
		pause = True
	else:
		pygame.mixer.music.unpause()
		pause=False

def display():
	global time
	os.system('clear')
	for i in range(len(songs)):
		if i == current:
			print(colored(songs[i].replace('\n',''), 'blue'))
		elif i == playing:
			print(colored(songs[i].replace('\n',''), 'green'))
		else:
			print(songs[i].replace('\n',''))
	if time == True:
		print(pygame.mixer.music.get_pos()) 


def main():
	global time
	global current
	while not exit:
		if time == True:
			display()
		key = readchar.readkey()
		if(key == 'k'):
			current -=1
			if current<1:
				current = 0
			display()
		if(key == 'm'):
			current +=1
			if current>len(songs)-1:
				current = len(songs)-1
			display()
		if(key == 'n'):
			time=True
			play(current)
			display()
		if(key == 'j'):
			stop()
		if(key == 'q'):
			os.system('clear')
			quit()


main()