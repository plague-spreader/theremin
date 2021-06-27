#!/usr/bin/env python

import argparse
import pygame
import numpy as np

notes = "A A# B C C# D D# E F F# G G#".split()
def get_note_from_exponent(i, display_cents=True):
	"""
	Given an exponent of the formula 440*2**(i/12)
	return the corresponding note. When i = 0 the
	note is A4 (which is 440 Hz).
	
	NOTE: i can be a fractional number.
	"""
	
	int_i = np.floor(i).astype(int)
	note = notes[int_i % 12]
	octave = int(int_i / 12) + 4
	cents = int((i - int_i)*100)
	if not display_cents:
		return "{}{}".format(note, octave)
	return "{}{}{:+d}".format(note, octave, cents)

def main(args):
	(max_x, max_y) = args.size
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()
	current_note_font = pygame.font.SysFont("monospace", 30)
	indicator_note_font = pygame.font.SysFont("monospace", int(max_x/48-15))
	screen = pygame.display.set_mode((max_x, max_y))
	# the note duration will be 0.1 seconds sampled at 44100 Hz
	dt = np.arange(0, 0.1, 1/44100).astype(np.float32)
	try:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					raise KeyboardInterrupt
			(x, y) = pygame.mouse.get_pos()
			(t_x, t_y) = ((x/max_x - 0.5)*2*24, 1 - y/max_y)
			freq = 440*2**(t_x/12)
			text = current_note_font.render(" Note: {} Volume: {}%".format(\
get_note_from_exponent(t_x), int(t_y*100)), False, (255, 255, 255))
			# graphics rendering stuff
			screen.fill((0, 0, 0,))
			for (i, x) in [(i, int(i*max_x/48)) for i in range(48)]:
				screen.fill((255, 0, 0), (x, 0, 1, max_y))
				screen.blit(indicator_note_font.render(\
get_note_from_exponent(i - 24, False), False, (255, 0, 0)), (x, max_y - 50))
			screen.blit(text, (50, 50))
			pygame.display.flip()
			
			note_signal = np.sin(2*np.pi*freq*dt)
			sound = pygame.mixer.Sound(note_signal)
			sound.set_volume(t_y)
			sound.play()
			pygame.time.wait(50)
	except KeyboardInterrupt:
		pass

def parse_size(s):
	return map(int, s.split("x"))

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("--size", type=parse_size, default=(640, 480))
	main(ap.parse_args())
