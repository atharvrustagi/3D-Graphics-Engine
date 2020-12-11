import pygame as pg
import math as mt

# colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

disp = 650
window = (720, 720)
pg.font.init()
font = pg.font.SysFont("arial", 20)
x_text = font.render("X", True, white)
y_text = font.render("Y", True, white)
z_text = font.render("Z", True, white)


def o(k):
	return k + window[0]//2

def draw(s, e):
	win.fill(black)
	global alpha, beta
	alpha += -mt.radians((s[0] - e[0]) / 400)
	beta += mt.radians((s[1] - e[1]) / 400)

	# co-ordinates
	x1, x2 = int(disp*mt.cos(alpha)/2), int(disp*mt.sin(alpha)*mt.sin(beta)/2)
	y1, y2 = int(disp*mt.sin(alpha)/2), int(disp*mt.cos(alpha)*mt.sin(-beta)/2)
	z1, z2 = 0, int(disp*mt.cos(beta)/2)

	# rectangle
	# pg.draw.polygon(win, white, ((o(-x1), o(-x2)), (o(-y1), o(-y2)), (o(x1), o(x2)), (o(y1), o(y2))))
	
	# x-axis
	pg.draw.line(win, green, (o(-x1), o(-x2)), (o(x1), o(x2)))
	win.blit(x_text, (o(x1), o(x2)))
	# y-axis
	pg.draw.line(win, blue, (o(-y1), o(-y2)), (o(y1), o(y2)))
	win.blit(y_text, (o(y1), o(y2)))
	# z-axis
	pg.draw.line(win, red, (o(z1), o(-z2)), (o(z1), o(z2)))
	win.blit(z_text, (o(z1), o(-z2)))

	pg.display.update()

win = pg.display.set_mode(window)
run = True
drag = False
start = (0, 0)
end = (0, 0)
alpha = beta = 0

while run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
		elif event.type == pg.MOUSEBUTTONDOWN:
			drag = True
			start = pg.mouse.get_pos()
		elif event.type == pg.MOUSEBUTTONUP:
			drag = False
		elif drag and event.type == pg.MOUSEMOTION:
			end = pg.mouse.get_pos()

		# k = pg.key.get_pressed()
		# if k[pg.K_UP]:
		# 	print('up')
		# elif k[pg.K_DOWN]:
		# 	print('down')

	draw(start, end)
