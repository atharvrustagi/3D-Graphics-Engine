import pygame as pg
from math import *
from time import perf_counter as pf

# colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
grey_l = (200, 200, 200)
grey_d = (50, 50, 50)

disp = 650
window = (720, 720)
speed = 800
pg.font.init()
font = pg.font.SysFont("arial", 20)
x_text = font.render("X", True, white)
y_text = font.render("Y", True, white)
z_text = font.render("Z", True, white)
s = 100
s1 = 100
s2 = 200

# [face1 coordinates, face2 {opposite face1} coordinates]	(cyclic)
cuboid_1 = [(0,0,0),(s,0,0),(s,0,s),(0,0,s),(0,s,0),(s,s,0),(s,s,s),(0,s,s)]
cuboid_2 = [(-s2, -s2, s1), (-s1, -s2, s1), (-s1, -s2, s2), (-s2, -s2, s2), (-s2, -s1, s1), (-s1, -s1, s1), (-s1, -s1, s2), (-s2, -s1, s2)]

# centre = (0, 200, 0), along y-axis; radius = 100
circle_pts = []
angle = 0
while angle <= 2*pi:
	circle_pts.append((int(100*cos(angle)), 200, int(100*sin(angle))))
	angle += 0.1


def o(k):
	return int(k + window[0]/2)

def render(p, a, b):
	# p is a 3 element tuple -> (x, y, z), a -> alpha, b -> beta
	if p[0] >= 0:
		theta = -atan(-p[1]/(p[0]+1e-8)) + a
	else:
		theta = -(atan(-p[1]/(p[0]+1e-8)) + pi) + a
	x = o((p[0]**2 + p[1]**2)**0.5 * cos(theta))
	y = o(-p[2]*cos(b) + (p[0]**2 + p[1]**2)**0.5 * sin(b) * sin(theta))
	return (x, y)


def renders(pts, a, b):
	# pts -> list containing 3-dimensional points
	# theta = -atan(-p[1]/(p[0]+1e-8)) + a if a >= 0 else -(atan(-p[1]/(p[0]+1e-8)) + pi) + a
	return [(o((p[0]**2 + p[1]**2)**0.5 * cos((-atan(-p[1]/(p[0]+1e-8)) if p[0] >= 0 else (-pi-atan(-p[1]/(p[0]+1e-8)))) + a)),
				o(-p[2]*cos(b) + (p[0]**2 + p[1]**2)**0.5 * sin(b) * sin((-atan(-p[1]/(p[0]+1e-8)) if p[0] >= 0 else (-pi-atan(-p[1]/(p[0]+1e-8)))) + a)))
				for p in pts]


def cuboid(pts, alpha, beta):
	"""	coordinates (or points) are in the order [front surface(4, cyclic), back surface(4, cyclic)]	"""

	points = renders(pts, alpha, beta)
	
	# front and back
	pg.draw.polygon(win, white, points[:4])
	pg.draw.polygon(win, white, points[4:])
	# top and bottom
	pg.draw.polygon(win, white, [points[0], points[1], points[5], points[4]])
	pg.draw.polygon(win, white, [points[3], points[2], points[6], points[7]])
	# left and right
	pg.draw.polygon(win, white, [points[0], points[4], points[7], points[3]])
	pg.draw.polygon(win, white, [points[1], points[5], points[6], points[2]])

	# outlines
	# pg.draw.line(win, grey_d, renders(points[0:2], alpha, beta))
	# pg.draw.line(win, grey_d, renders(points[1:3], alpha, beta))
	# pg.draw.line(win, grey_d, renders(points[2:4], alpha, beta))
	for i in range(3):
		pg.draw.line(win, grey_d, points[i], points[i+1])
	for i in range(4, 7):
		pg.draw.line(win, grey_d, points[i], points[i+1])
	pg.draw.line(win, grey_d, points[0], points[4])
	pg.draw.line(win, grey_d, points[1], points[5])
	pg.draw.line(win, grey_d, points[2], points[6])
	pg.draw.line(win, grey_d, points[3], points[7])
	pg.draw.line(win, grey_d, points[0], points[3])
	pg.draw.line(win, grey_d, points[4], points[7])


def circle(pts, alpha, beta):
	cpts = renders(pts, alpha, beta)
	pg.draw.polygon(win, white, cpts)
	for c in range(len(cpts)-1):
		pg.draw.line(win, black, cpts[c], cpts[c+1], 2)
	pg.draw.line(win, black, cpts[-1], cpts[0], 2)
	

def draw(alpha, beta):
	win.fill(black)	

	# co-ordinates
	x1, x2 = disp*cos(alpha)/2, disp*sin(alpha)*sin(beta)/2
	y1, y2 = disp*sin(alpha)/2, disp*cos(alpha)*sin(-beta)/2
	z1, z2 = 0, disp*cos(beta)/2
	
	 # z-axis
	pg.draw.line(win, red, (o(z1), o(-z2)), (o(z1), o(z2)))
	win.blit(z_text, (o(z1), o(-z2)))
	# x-axis
	pg.draw.line(win, green, (o(-x1), o(-x2)), (o(x1), o(x2)))
	win.blit(x_text, (o(x1), o(x2)))
	# y-axis
	pg.draw.line(win, blue, (o(-y1), o(-y2)), (o(y1), o(y2)))
	win.blit(y_text, (o(-y1), o(-y2)))

	# shapes
	cuboid(cuboid_2, alpha, beta)
	cuboid(cuboid_1, alpha, beta)

	# circle
	circle(circle_pts, alpha, beta)

	pg.display.update()


win = pg.display.set_mode(window)
run = True
drag = False
start = (0, 0)
end = (0, 0)
alpha = 0
beta = 0
fps = 0
avg_fps = []
count = 0

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
		if not drag:
			start = end
    
	fps = pf()
	alpha += -radians((start[0] - end[0]) / speed)
	beta += radians((start[1] - end[1]) / speed)

	if alpha > 2*pi or alpha < -2*pi:
		alpha = 0
	if beta > 2*pi or beta < -2*pi:
		beta = 0

	draw(alpha, beta)

	fps = round(1/(pf()-fps))
	avg_fps.append(fps)
	count += 1
	print(f"FPS: {fps}")

s = 0
for i in range(count):
	s += avg_fps[i]

print(f"\nAverage FPS: {round(s/count)}")
