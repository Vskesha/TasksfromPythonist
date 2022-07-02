import pygame
import time
import random

dis_width = 600
dis_height = 400
snake_speed = 1
speed_adjust = False
snake_block = 25
snake_border = round(snake_block / 20)
size_of_food = 20
border = round(30 / snake_block) * snake_block

white = (255, 255, 255)
yellow = 'yellow'
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

pygame.init()
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змійка by VsKesha')
clock = pygame.time.Clock()

def get_food(snake):
	x = round(random.randrange(border, dis_width - snake_block - border) / snake_block) * snake_block
	y = round(random.randrange(border, dis_height - snake_block - border) / snake_block) * snake_block
	for x1, y1 in snake:
		if x == x1 and y == y1:
			x, y = get_food(snake)
	return [x, y]

def your_score(score=0):
	score_font = pygame.font.SysFont("comicsansms", 35)
	value = score_font.render("Рахунок: " + str(score), True, yellow)
	dis.blit(value, [0, 0])
	pygame.display.update()

def your_speed(speed=1):
	speed_font = pygame.font.SysFont("comicsansms", 35)
	value = speed_font.render("Швидкість: " + str(speed), True, yellow)
	dis.blit(value, [dis_width - 180, 0])
	pygame.display.update()

def show_message(msg, color, coords=[dis_width/7, dis_height/3], font_size=30):
	font_style = pygame.font.SysFont("comicsansms", font_size)
	mesg = font_style.render(msg, True, color)#.set_alpha(100)
	dis.blit(mesg, coords)
	pygame.display.update()

def refresh_screen():
	#makes grid on the screen
		dis.fill('black')
		for i in range(border + snake_block, dis_width - snake_block, snake_block):
			pygame.draw.line(dis, 'grey10', [i, border], [i, dis_height - border], snake_border * 2)
		for i in range(border + snake_block, dis_height - snake_block, snake_block):
			pygame.draw.line(dis, 'grey10', [border, i], [dis_width - border, i], snake_border * 2)
		border_points = [
			[border, border],
			[dis_width - border - snake_border, border],
			[dis_width - border - snake_border, dis_height - border - snake_border],
			[border, dis_height - border - snake_border]]
		pygame.draw.lines(dis, (150, 150, 150), True, border_points, snake_border * 2)

def draw_food(foodx, foody):
	pygame.draw.circle(dis, 'yellow', [foodx + round(snake_block / 2), foody + round(snake_block / 2)], size_of_food / 2)
	pygame.draw.circle(dis, blue, [foodx + round(snake_block / 2), foody + round(snake_block / 2)], size_of_food / 3)


def draw_snake(snake, direct):
	
	#draw tail
	if len(snake) > 1:
		tail = snake[0]
		previos = snake[1]
		t1 = []
		t2 = []
		t3 = []
		if tail[0] > previos[0]: #tail goes left
			t1 = [tail[0] + 1, tail[1] + 1]
			t2 = [tail[0] + 1, tail[1] + snake_block - 1]
			t3 = [tail[0] + snake_block, tail[1] + round(snake_block / 2)]
		if tail[0] < previos[0]: #tail goes right
			t1 = [tail[0] + snake_block - 1, tail[1] + 1]
			t2 = [tail[0] + snake_block - 1, tail[1] + snake_block - 1]
			t3 = [tail[0], tail[1] + round(snake_block / 2)]
		else:
			if tail[1] > previos[1]: #tail goes up
				t1 = [tail[0] + 1, tail[1] + 1]
				t2 = [tail[0] + snake_block - 1, tail[1] + 1]
				t3 = [tail[0] + round(snake_block / 2), tail[1] + snake_block]
			elif tail[1] < previos[1]: # tail goes down
				t1 = [tail[0] + 1, tail[1] + snake_block - 1]
				t2 = [tail[0] + snake_block - 1, tail[1] + snake_block - 1]
				t3 = [tail[0] + round(snake_block / 2), tail[1]]
		points = [t1, t2, t3]
		pygame.draw.polygon(dis, green, points)
		pygame.draw.polygon

	#draw body of snake
	for x in snake[1:-1]:
		pygame.draw.rect(dis, green, [x[0] + 1, x[1] + 1, snake_block - 2, snake_block -2])
	
	#draw_head(snake)
	head = snake[-1]
	center = [head[0] + round(snake_block / 2), head[1] + round(snake_block / 2)]
	head_radius = snake_block / 1.4
	pygame.draw.circle(dis, green, [center[0], center[1]], head_radius)
	
	#draw_eyes and tongue
	eyes_color = 'white'
	tongue_color = 'red'
	eye_size = head_radius * 0.35
	distance_forward = round(head_radius * 0.4)
	distance_between_eyes = round(head_radius * 0.5)
	tongue_length = round(head_radius * 0.3)
	tongue_thickness = round(head_radius * 0.05)
	eye_coord1 = []
	eye_coord2 = []	 
	tongue_coord = []
	if not direct:
		direct = 'right'
	if direct == 'up':
		eye_coord1 = [center[0] - distance_between_eyes, center[1] - distance_forward]
		eye_coord2 = [center[0] + distance_between_eyes, center[1] - distance_forward]
		tongue_coord = [center[0] - tongue_thickness, center[1] - head_radius - tongue_length, tongue_thickness * 2, tongue_length]
	elif direct == 'down':
		eye_coord1 = [center[0] - distance_between_eyes, center[1] + distance_forward]
		eye_coord2 = [center[0] + distance_between_eyes, center[1] + distance_forward]
		tongue_coord = [center[0] - tongue_thickness, center[1] + head_radius, tongue_thickness * 2, tongue_length]
	elif direct == 'left':
		eye_coord1 = [center[0] - distance_forward, center[1] + distance_between_eyes]
		eye_coord2 = [center[0] - distance_forward, center[1] - distance_between_eyes]
		tongue_coord = [center[0] - head_radius - tongue_length, center[1] - tongue_thickness, tongue_length, tongue_thickness * 2]
	elif direct == 'right':
		eye_coord1 = [center[0] + distance_forward, center[1] - distance_between_eyes]
		eye_coord2 = [center[0] + distance_forward, center[1] + distance_between_eyes]	 
		tongue_coord = [center[0] + head_radius, center[1] - tongue_thickness, tongue_length, tongue_thickness * 2]
	pygame.draw.circle(dis, eyes_color, eye_coord1, eye_size)
	pygame.draw.circle(dis, 'black', eye_coord1, eye_size / 2)
	pygame.draw.circle(dis, eyes_color, eye_coord2, eye_size)
	pygame.draw.circle(dis, 'black', eye_coord2, eye_size / 2)
	pygame.draw.rect(dis, tongue_color, tongue_coord)
	pygame.draw.ellipse

def game_menu():
	global snake_speed
	global speed_adjust
	refresh_screen()
	your_score()
	your_speed()
	menu_bg = pygame.Surface([dis_width, dis_height])#.set_alpha(50)
	pygame.draw.rect(menu_bg, 'grey20', [0, 0, dis_width, dis_height])
	menu_bg.set_alpha(200)
	dis.blit(menu_bg, [0, 0])
	show_message("ЗМІЙКА", "grey5", [dis_width / 2 - 100, border], 80)
	show_message("by vskesha", "dark green", [dis_width / 2 + 100, border + 50], 30)
	x = dis_width / 2 - 200
	y = dis_height / 2
	show_message("Вибери швидкість:", 'black', [x, y], 50)
	show_message('"1" - "9" вибрати швидкість', 'black', [x, y +50], 30)
	show_message('"A" - автоматично', 'black', [x, y + 80], 30)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_close()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					game_close()
				elif event.key == pygame.K_a:
					speed_adjust = True
					break
				elif event.key == pygame.K_1:
					snake_speed = 1
					break
				elif event.key == pygame.K_2:
					snake_speed = 2
					break
				elif event.key == pygame.K_3:
					snake_speed = 3
					break
				elif event.key == pygame.K_4:
					snake_speed = 4
					break
				elif event.key == pygame.K_5:
					snake_speed = 5
					break
				elif event.key == pygame.K_6:
					snake_speed = 6
					break
				elif event.key == pygame.K_7:
					snake_speed = 7
					break
				elif event.key == pygame.K_8:
					snake_speed = 8
					break
				elif event.key == pygame.K_9:
					snake_speed = 9
					break
		else:
			continue
		break

def game_pause():
	#print("GAME PAUSED")
	paused = True
	x = dis_width / 4
	y = dis_height / 3
	show_message("ПАУЗА!", red, [x, y] , 50)
	show_message("Нажми С для продовження", red, [x, y + 65], 35)
	show_message("Нажми Q щоб вийти", red, [x, y + 100], 35)
	
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_close()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					#print("GAME RESUMED")
					paused = False
				if event.key == pygame.K_q:
					game_close()
					
def game_close():
	pygame.quit()
	quit()

def game_over():
	while True:
		x = dis_width / 4
		y = dis_height / 3
		show_message("ПОРАЗКА!", red, [x, y] , 50)
		show_message("Нажми С - нова гра", red, [x, y + 65], 35)
		show_message("Нажми Q - вийти", red, [x, y + 100], 35)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_close()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					game_close()
				if event.key == pygame.K_c:
					gameLoop()

def gameLoop():	
	
	# getting start position of the snake
	x1 = round(dis_width / 2 / snake_block) * snake_block
	y1 = round(dis_height / 2 / snake_block) * snake_block
	direction = 'right'
	snake_List = []
	Length_of_snake = 3
	Score = 0
	foodx, foody = get_food(snake_List)
	global snake_speed
	global speed_adjust
	game_menu()

	while True:
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				game_close()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					game_pause()
				elif event.key == pygame.K_q:
					game_close()
				elif event.key == pygame.K_LEFT and direction != 'right':
					direction = 'left'
				elif event.key == pygame.K_RIGHT and direction != 'left':
					direction = 'right'
				elif event.key == pygame.K_UP and direction != 'down':
					direction = 'up'
				elif event.key == pygame.K_DOWN and direction != 'up':
					direction = 'down'
		
		if direction == 'left': x1 -= snake_block
		elif direction == 'right': x1 += snake_block
		elif direction == 'up': y1 -= snake_block
		elif direction == 'down': y1 += snake_block
		
		if x1 >= dis_width - border or x1 < border or y1 >= dis_height - border or y1 < border:
			game_over()
			
		snake_head = [x1, y1]
		snake_List.append(snake_head)
		if len(snake_List) > Length_of_snake:
			del snake_List[0]

		for x in snake_List[:-1]:
			if x == snake_head:
				game_over()
		
		refresh_screen()
		draw_food(foodx, foody)
		draw_snake(snake_List, direction)
		your_score(Score)
		your_speed(snake_speed)
				
		if x1 == foodx and y1 == foody:
			show_message("Нямм", 'yellow', [foodx + snake_block, foody + snake_block])
			foodx, foody = get_food(snake_List)
			Length_of_snake += 1
			Score += snake_speed
		if speed_adjust:
			snake_speed = 1 + (Length_of_snake - 3)// 10
		clock.tick(snake_speed)

	
gameLoop()