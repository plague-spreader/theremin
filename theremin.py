#!/usr/bin/env python

import argparse
import subprocess
import time

def system(s):
	"""
	Utility function for executing system commands
	"""
	return tuple(map(lambda t: t.decode(), subprocess.Popen(s.split(), \
stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()))

def system_bg(s):
	"""
	Utility function for executing system commands in background
	"""
	subprocess.Popen(s.split())

def main(args):
	# one-liner for retrieving the screen size using xdpyinfo
	(max_x, max_y) = map(int, (next(filter(lambda t: "dimensions" in t, \
system("xdpyinfo")[0].split("\n"))).split()[1].split()[0]).split("x"))
	while True:
		# one-liner for retrieving the mouse coordinates using xdotool
		(x, y, _, _) = map(lambda t: int(t.split(":")[1]), \
system("xdotool getmouselocation")[0].split())
		(t_x, t_y) = ((x/max_x - 0.5)*2*24, 1 - y/max_y)
		freq = 440*2**(t_x/12)
		system_bg("play -n synth .1 sine {} vol {}".format(freq, t_y))
		time.sleep(0.05)

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	main(ap.parse_args())
