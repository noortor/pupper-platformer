import simplegui
import math

WIDTH = 1000
HEIGHT = 800 
player_width = 60
player_height = 85


jump_count = 0
shuriken_count = 0
player_hp = 100
player_hp_topleft = [25, 20]
player_hp_bottomleft = [25, 45]
player_hp_topright = [25 + player_hp*2, 20]
player_hp_bottomright = [25 + player_hp*2, 45]
player_hp_color = "Green"
player_direction = "right"
shuriken_width = 50
shuriken_height = 50
shuriken_vel = [0, 0]
shuriken_pos = [0, 0]
shuriken_angle = 0
shuriken_spin_rate = 0

platform1_topleft = [WIDTH - 200, HEIGHT - 120] 
platform1_bottomleft = [WIDTH - 200, HEIGHT - 100]
platform1_topright = [WIDTH, HEIGHT - 120]
platform1_bottomright = [WIDTH, HEIGHT - 100]

platform2_topleft = [WIDTH/2 - 200, 3*HEIGHT/4]
platform2_bottomleft = [WIDTH/2 -200, 3*HEIGHT/4 + 20]
platform2_topright = [WIDTH/2 + 150, 3*HEIGHT/4]
platform2_bottomright = [WIDTH/2 + 150, 3*HEIGHT/4 + 20]

platform3_topleft = [0, HEIGHT/2 + 100]
platform3_bottomleft = [0, HEIGHT/2 + 120]
platform3_topright = [200, HEIGHT/2 + 100]
platform3_bottomright = [200, HEIGHT/2 + 120]

platform4_topleft = [WIDTH-160, HEIGHT/2 + 40]
platform4_bottomleft = [WIDTH-160, HEIGHT/2 + 60]
platform4_topright = [WIDTH, HEIGHT/2 + 40]
platform4_bottomright = [WIDTH, HEIGHT/2 + 60]

platform5_topleft = [WIDTH/2-80, HEIGHT/2 - 80]
platform5_bottomleft = [WIDTH/2-80, HEIGHT/2 - 60]
platform5_topright = [WIDTH/2 + 200, HEIGHT/2 - 80]
platform5_bottomright = [WIDTH/2 + 200, HEIGHT/2 - 60]

platform6_topleft = [WIDTH-120, 200]
platform6_bottomleft = [WIDTH-120, 220]
platform6_topright = [WIDTH, 200]
platform6_bottomright = [WIDTH, 220]

platform7_topleft = [200, 240]
platform7_bottomleft = [200, 260]
platform7_topright = [320, 240]
platform7_bottomright = [320, 260]

enemy_height = 100
enemy_width = 100
enemy1_pos = [platform1_topleft[0] + enemy_width/2, platform1_topleft[1] - enemy_height/2]
enemy2_pos = [platform3_topright[0] - enemy_width/2, platform3_topleft[1] - enemy_height/2]
enemy3_pos = [platform6_topleft[0] + enemy_width/2, platform6_topleft[1] - enemy_height/2] 
enemy_pos = [[enemy1_pos[0], enemy1_pos[1]], [enemy2_pos[0], enemy2_pos[1]], [enemy3_pos[0], enemy3_pos[1]]]
enemy_right = [enemy1_pos[0] + enemy_width/2, enemy2_pos[0] + enemy_width/2, enemy3_pos[0] + enemy_width/2]
enemy_left = [enemy1_pos[0] - enemy_width/2, enemy2_pos[0] - enemy_width/2, enemy3_pos[0] - enemy_width/2]
enemy_top = [enemy1_pos[1] - enemy_height/2, enemy2_pos[1] - enemy_height/2, enemy3_pos[1] - enemy_height/2]
enemy_bottom = [enemy1_pos[1] + enemy_height/2, enemy2_pos[1] + enemy_height/2, enemy3_pos[1] + enemy_height/2]


laser_speed = 8

goal_width = 100
goal_height = 100
goal_pos = [platform7_topleft[0] + 60, platform7_topleft[1] - 60]

def new_game():
    global player_hp, start, player_pos, player_vel, scene, player_hp_color, enemy_alive, enemy_kills, shuriken_shot, laser_shot, laser_update, laser_pos, laser_vel, laser_angle
    global laser_height, laser_width, laser_frontHeight, laser_frontWidth, jump
    jump = False
    scene = "start"
    player_hp = 100
    start = False
    player_pos = [100, HEIGHT - player_height/2.0]
    player_vel = [0, 0]
    player_hp_color = "Green"
    enemy_alive = [True, True, True]
    enemy_kills = 0
    shuriken_shot = False
    #variables for all lasers are stored in lists for easy access
    laser_shot = [False, False, False]
    laser_update = [False, False, False]
    laser_pos = [[enemy1_pos[0], enemy1_pos[1]], [enemy2_pos[0], enemy2_pos[1]], [enemy3_pos[0], enemy3_pos[1]]] 
    laser_vel = [[0, 0], [0, 0], [0, 0]]
    laser_angle = [0, 0, 0]
    laser_height = [16, 16, 16]
    laser_width = [60, 60, 60]
    laser_frontHeight = [0, 0, 0]
    laser_frontWidth = [0, 0, 0]
    
def health_control():
    global player_hp, player_hp_color, player_hp_topright, player_hp_bottomright, scene 
    if player_hp <= 0:
        scene = "game_over"
    elif player_hp < 25:
        player_hp_color = "Red"
    elif player_hp < 50:
        player_hp_color = "Yellow"
    player_hp_topright = [25 + player_hp*2, 20]
    player_hp_bottomright = [25 + player_hp*2, 45] 

def goal_control():
    global player_pos, player_vel, player_width, player_height, scene, goal_pos, goal_width, goal_height
    if enemy_kills == 3:       
        #player lands on goal ring
        if goal_pos[1] - goal_height/2 + player_vel[1] >= player_pos[1]+player_height/2.0 and goal_pos[1] - goal_height/2 <= player_pos[1]+player_height/2.0:
            if player_pos[0] - player_width/2<= goal_pos[0] + goal_width/2 and player_pos[0]+player_width/2 >= goal_pos[0] - goal_width/2 and jump_count > 0.5:
                scene = "win"   
        #player hits right or left of goal ring
        if player_pos[1] +player_height/2 >= goal_pos[1] - goal_height/2 and player_pos[1] - player_width/2 <= goal_pos[1] + goal_height/2:
            if player_pos[0] + player_width/2 >= goal_pos[0] - goal_width/2 and player_pos[0] - player_width/2 <= goal_pos[0] - goal_width/2 +player_vel[0]:
                scene = "win"
            if player_pos[0] - player_width/2 <= goal_pos[0] + goal_width/2 and player_pos[0] - player_width/2 >= goal_pos[0] + goal_width/2+player_vel[0]:
                scene = "win"
                
def shuriken_control():
    global shuriken_shot, shuriken_pos, shuriken_vel, player_pos, player_direction, shuriken_spin_rate, shuriken_angle, shuriken_count
    if shuriken_shot == False:
        shuriken_count = 0
        shuriken_pos[0]= player_pos[0]
        shuriken_pos[1]= player_pos[1]
        shuriken_vel[1] = 0
        shuriken_vel[0] = 0
        shuriken_angle = 0
        shuriken_spin_rate = 0
    elif player_direction == "right" and shuriken_vel[0]!=-10:
        shuriken_vel[0] = 10
        shuriken_spin_rate = 1
        shuriken_count += 1.0/60
        shuriken_vel[1]=-(3 - (6 * shuriken_count))
    elif player_direction == "left" and shuriken_vel[0]!=10:
        shuriken_vel[0] = -10
        shuriken_spin_rate = -1
        shuriken_count += 1.0/60
        shuriken_vel[1]=-(3 - (6 * shuriken_count))
    if shuriken_pos[0] + shuriken_width/2> WIDTH or shuriken_pos[0] - shuriken_width/2 < 0:
        shuriken_vel[0] = 0
        shuriken_shot = False
        shuriken_angle = 0
        shuriken_spin_rate = 0
    if shuriken_pos[1] + shuriken_height/2> HEIGHT or shuriken_pos[1] - shuriken_height/2 < 0:    
        shuriken_vel[0] = 0
        shuriken_shot = False
        shuriken_angle = 0
        shuriken_spin_rate = 0
        
def enemy_control():
    global laser_shot, laser_pos, laser_angle, laser_update, laser_height, laser_width, laser_speed, laser_vel, enemy_pos, enemy_width, enemy_height, enemy_alive, player_pos, player_vel, laser_frontHeight, laser_frontWidth, shuriken_pos, shuriken_vel, shuriken_shot
    global enemy_right, enemy_left, player_hp, enemy_kills
    for i in range(len(laser_pos)):
        if laser_shot[i] == False:
            laser_pos[i][0] = enemy_pos[i][0]
            laser_pos[i][1] = enemy_pos[i][1]          
            laser_angle[i] = 0
        if enemy_alive[i] == True:
            if ((player_pos[1]-enemy_pos[i][1])**2 + (player_pos[0]-enemy_pos[i][0])**2)**(1.0/2) <= 1000 and laser_shot[i] == False and abs(enemy_pos[i][1] - player_pos[1])<=abs((-math.sqrt(111.0)/17)*(enemy_pos[i][0]-player_pos[0])):
                laser_shot[i] = True
                laser_update[i] = True
        if laser_shot[i] == True and laser_update[i] == True: 
            laser_update[i] = False
            if enemy_pos[i][0]-player_pos[0]>=0:
                laser_angle[i] = math.pi + math.atan((player_pos[1]-enemy_pos[i][1])/(player_pos[0]-enemy_pos[i][0]))
            else: 
                laser_angle[i] = math.atan((player_pos[1]-enemy_pos[i][1])/(player_pos[0]-enemy_pos[i][0]))
            laser_vel[i][0] = math.cos(laser_angle[i]) * laser_speed 
            laser_vel[i][1] = math.sin(laser_angle[i]) * laser_speed   
            laser_frontHeight = abs(math.sin(math.pi/2.0 - laser_angle[i]) * 16)
            laser_frontWidth = abs(math.cos(math.pi/2.0 - laser_angle[i]) * 16)
            laser_height[i] = abs(abs(math.sin(laser_angle[i]) * 60) - laser_frontHeight)
            laser_width[i] = abs(abs(math.cos(laser_angle[i]) * 60) - laser_frontWidth)
        if laser_pos[i][1] + laser_height[i]/2> HEIGHT or laser_pos[i][1] - laser_height[i]/2 < 0 or laser_pos[i][0] + laser_width[i]/2> WIDTH or laser_pos[i][0] - laser_width[i]/2 < 0:    
            laser_vel[i][0] = 0
            laser_vel[i][1] = 0
            laser_shot[i] = False
        laser_pos[i][0] += laser_vel[i][0]
        laser_pos[i][1] += laser_vel[i][1]
        if enemy_alive[i] == True:
        #shuriken hits top of enemy 
            if shuriken_pos[0] - shuriken_width/2<= enemy_right[i] and shuriken_pos[0]+shuriken_width/2 >= enemy_left[i]:
                if enemy_top[i] + shuriken_vel[1] >= shuriken_pos[1] + shuriken_height/2 and enemy_top[i] <= shuriken_pos[1]+shuriken_height/2 and shuriken_count > 0.5:
                    shuriken_shot = False 
                    enemy_alive[i] = False
                    enemy_kills += 1
        #shuriken hits left or right of enemy
            if (shuriken_pos[1] + shuriken_height/2 >= enemy_top[i] and shuriken_pos[1] - shuriken_height/2 <= enemy_pos[i][1]) or (shuriken_pos[1] + shuriken_height/2 <= enemy_bottom[i] and shuriken_pos[1]+shuriken_height/2 >= enemy_pos[i][1]):
                if enemy_left[i] - shuriken_vel[0] <= shuriken_pos[0] + shuriken_width/2 and enemy_left[i] >= shuriken_pos[0] + shuriken_width/2:
                    shuriken_shot = False
                    enemy_alive[i] = False
                    enemy_kills += 1
                if enemy_right[i] - shuriken_vel[0] >= shuriken_pos[0] - shuriken_width/2 and enemy_right[i] <= shuriken_pos[0] - shuriken_width/2:
                    shuriken_shot = False    
                    enemy_alive[i] = False
                    enemy_kills += 1
    #laser hits top or bottom of player
        if laser_pos[i][0] - laser_width[i]/2<= player_pos[0]+player_width/2 and laser_pos[i][0] + laser_width[i]/2 >= player_pos[0]-player_width/2 and laser_shot[i] == True:
            if player_pos[1]-player_height/2 + laser_vel[i][1] -player_vel[1]>= laser_pos[i][1] + laser_height[i]/2 and player_pos[1]-player_height/2 <= laser_pos[i][1] + laser_height[i]/2:
                laser_shot[i] = False
                player_hp -= 20
            if player_pos[1]+player_height/2 + laser_vel[i][1] -player_vel[1]<= laser_pos[i][1] + laser_height[i]/2and player_pos[1]+player_height/2 >= laser_pos[i][1] - laser_height[i]/2:
                laser_shot[i] = False
                player_hp -= 20
    #laser hits left or right of player 
        if laser_pos[i][1] + laser_height[i]/2 >= player_pos[1]-player_height/2 and laser_pos[i][1] - laser_height[i]/2 <= player_pos[1]+player_height/2 and laser_shot[i] == True:
            if player_pos[0]-player_width/2 - laser_vel[i][0] +player_vel[0] <= laser_pos[i][0] + laser_width[i]/2 and player_pos[0]-player_width/2 >= laser_pos[i][0] + laser_width[i]/2:
                laser_shot[i] = False
                player_hp -= 20
            if player_pos[0]+player_width/2 - laser_vel[i][0] +player_vel[0] >= laser_pos[i][0] - laser_width[i]/2 and player_pos[0]+player_width/2 <= laser_pos[i][0] - laser_width[i]/2:
                laser_shot[i] = False
                player_hp -= 20
                
def jump_control():
    global jump, HEIGHT, WIDTH, player_vel, jump_count, player_pos
    if jump == True:
        jump_count+=1.0/60
        player_vel[1]=-((40.0/3) - ((80.0/3) * jump_count))
    if jump == True and player_pos[1] > HEIGHT-player_height/2.0:
        jump = False
        player_vel[1] = 0
        jump_count = 0
        player_pos[1]=HEIGHT-player_height/2.0
        
def side_boundaries():
    global player_pos, player_vel, WIDTH
    if player_pos[0]+player_width/2 > WIDTH:
        player_vel[0] = 0
        player_pos[0] -= 4
    if player_pos[0]-player_width/2 < 0:
        player_vel[0] = 0
        player_pos[0] += 4    
        
def movement_updates():
    global player_pos, player_vel, shuriken_pos, shuriken_vel, shuriken_angle, shuriken_spin_rate 
    player_pos[0]+=player_vel[0]
    player_pos[1]+=player_vel[1]
    shuriken_pos[0] += shuriken_vel[0]
    shuriken_pos[1] += shuriken_vel[1]
    shuriken_angle += shuriken_spin_rate
    
    
def platform_collision(platform_x1, platform_x2, platform_y1, platform_y2):
    global player_pos, player_height, player_vel, jump, jump_count, shuriken_pos, shuriken_vel, shuriken_width, shuriken_height, shuriken_count, shuriken_shot, laser_height, laser_width, laser_pos, laser_vel, laser_frontHeight, laser_frontWidth
    #player lands on platform or falls from platform
    if platform_y1 + player_vel[1] >= player_pos[1]+player_height/2.0 and platform_y1 <= player_pos[1]+player_height/2.0:
        if player_pos[0] - player_width/2<= platform_x2 and player_pos[0]+player_width/2 >= platform_x1 and jump_count > 0.5:
            jump = False
            player_vel[1] = 0
            player_pos[1] = platform_y1 - player_height/2.0
            jump_count = 0
        if (player_pos[0]-player_width/2 > platform_x2 or player_pos[0]+player_width/2 < platform_x1) and player_vel[1]==0:
            if player_pos[0]-player_width/2 < platform_x2+player_width and player_pos[0]+player_width/2 > platform_x1-player_width:
                jump_count = 0.5
                jump = True
    #player jumps up into platform
    if platform_y2 + player_vel[1] <= player_pos[1]-player_height/2.0 and platform_y2 >= player_pos[1]-player_height/2.0:
        if player_pos[0] - player_width/2<= platform_x2 and player_pos[0]+player_width/2 >= platform_x1:
            jump_count = 0.8-jump_count
    #player hits right or left of platform
    if player_pos[1] +player_height/2 >= platform_y1 and player_pos[1] - player_width/2 <= platform_y2:
        if player_pos[0] + player_width/2 >= platform_x1 and player_pos[0] - player_width/2 <= platform_x1+player_vel[0]:
            player_vel[0] = 0
            player_pos[0] -= 4
        if player_pos[0] - player_width/2 <= platform_x2 and player_pos[0] - player_width/2 >= platform_x2+player_vel[0]:
            player_vel[0] = 0
            player_pos[0] += 4
    #shuriken hits top or bottom of platform
    if shuriken_pos[0] - shuriken_width/2<= platform_x2 and shuriken_pos[0]+shuriken_width/2 >= platform_x1:
        if platform_y1 + shuriken_vel[1] >= shuriken_pos[1] + shuriken_height/2 and platform_y1 <= shuriken_pos[1]+shuriken_height/2 and shuriken_count > 0.5:
            shuriken_shot = False
        if platform_y2 + shuriken_vel[1] <= shuriken_pos[1] and platform_y2 >= shuriken_pos[1] - shuriken_height/2:
            shuriken_shot = False
    #shuriken hits left or right of platform
    if shuriken_pos[1] +shuriken_height/2 >= platform_y1 and shuriken_pos[1] - shuriken_height/2 <= platform_y2:
        if platform_x1 - shuriken_vel[0] <= shuriken_pos[0] + shuriken_width/2 and platform_x1 >= shuriken_pos[0] + shuriken_width/2:
            shuriken_shot = False
        if platform_x2 - shuriken_vel[0] >= shuriken_pos[0] - shuriken_width/2 and platform_x2 <= shuriken_pos[0] - shuriken_width/2:
            shuriken_shot = False
    for i in range(len(laser_pos)):
    #laser hits top or bottom of platform
        if laser_pos[i][0] - laser_width[i]/2<= platform_x2 and laser_pos[i][0] + laser_width[i]/2 >= platform_x1:
            if platform_y1 + laser_vel[i][1] >= laser_pos[i][1] + laser_height[i]/2 and platform_y1 <= laser_pos[i][1] + laser_height[i]/2:
                laser_shot[i] = False
            if platform_y2 + laser_vel[i][1] <= laser_pos[i][1] + laser_height[i]/2and platform_y2 >= laser_pos[i][1] - laser_height[i]/2:
                laser_shot[i] = False
    #laser hits left or right of platform 
        if laser_pos[i][1] + laser_height[i]/2 >= platform_y1 and laser_pos[i][1] - laser_height[i]/2 <= platform_y2:
            if platform_x1 - laser_vel[i][0] <= laser_pos[i][0] + laser_width[i]/2 and platform_x1 >= laser_pos[i][0] + laser_width[i]/2:
                laser_shot[i] = False
            if platform_x2 - laser_vel[i][0] >= laser_pos[i][0] - laser_width[i]/2 and platform_x2 <= laser_pos[i][0] - laser_width[i]/2:
                laser_shot[i] = False
def draw(canvas):
    if scene == "start":
        canvas.draw_image(start_background, (1920/2, 1080/2), (1920, 1080), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))
        canvas.draw_text('The Adventures of', (WIDTH/2-299.5, HEIGHT/6.0),80 , "White")
        canvas.draw_text('the Legendary Pupper', (WIDTH/2-353, HEIGHT/3.0),80 , "White")
        canvas.draw_text('Press i for instructions', (WIDTH/2-179, HEIGHT - 50), 40, "White")
        canvas.draw_text('Press the space bar to begin', (WIDTH/2-277, HEIGHT - 100), 50, "White")
    elif scene == "scene_instructions":
        canvas.draw_image(instructions_background, (736/2, 552/2), (736, 552), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))
        canvas.draw_text("Instructions", (WIDTH/2-188.5, HEIGHT/6.0), 80, "Black")
        canvas.draw_text("w: jump", (150, HEIGHT/2-100), 50, "Black")
        canvas.draw_text("a: left", (150, HEIGHT/2-50), 50, "Black")
        canvas.draw_text("d: right", (150, HEIGHT/2), 50, "Black")
        canvas.draw_text("space: throw shuriken", (150, HEIGHT/2+50), 50, "Black")
        canvas.draw_text('Press the space bar to begin', (WIDTH/2-277, HEIGHT - 50), 50, "Black")
    elif scene == "scene1":
        canvas.draw_image(background1, (1248/2, 1200/2), (1248, 1200), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))  
        canvas.draw_polygon([platform1_topleft, platform1_bottomleft, platform1_bottomright, platform1_topright], 2, "Black", "Blue")
        canvas.draw_polygon([platform2_topleft, platform2_bottomleft, platform2_bottomright, platform2_topright], 2, "Black", "Blue")
        canvas.draw_polygon([platform3_topleft, platform3_bottomleft, platform3_bottomright, platform3_topright], 2, "Black", "Blue")
        canvas.draw_polygon([platform4_topleft, platform4_bottomleft, platform4_bottomright, platform4_topright], 2, "Black", "Blue")
        canvas.draw_polygon([platform5_topleft, platform5_bottomleft, platform5_bottomright, platform5_topright], 2, "Black", "Blue")
        canvas.draw_polygon([platform6_topleft, platform6_bottomleft, platform6_bottomright, platform6_topright], 2, "Black", "Blue")
        canvas.draw_polygon([platform7_topleft, platform7_bottomleft, platform7_bottomright, platform7_topright], 2, "Black", "Blue")
        canvas.draw_polygon([player_hp_topleft, player_hp_bottomleft, player_hp_bottomright, player_hp_topright], 1.5, "Black", player_hp_color)
        if enemy_kills == 3:
            canvas.draw_image(goal, (575, 500), (900, 900), (goal_pos[0], goal_pos[1]), (100, 100))
        if enemy_alive[0] == True:	
            canvas.draw_image(enemy, (1000/2, 1165.0/2), (1000, 1165), (enemy1_pos[0], enemy1_pos[1]), (80, 100))
        if enemy_alive[1] == True:	
            canvas.draw_image(enemy, (1000/2, 1165.0/2), (1000, 1165), (enemy2_pos[0], enemy2_pos[1]), (80, 100))
        if enemy_alive[2] == True:
            canvas.draw_image(enemy, (1000/2, 1165.0/2), (1000, 1165), (enemy3_pos[0], enemy3_pos[1]), (80, 100))
        canvas.draw_text('Hp: '+ str(player_hp), (70, 70), 30, "Black")
        if player_direction == "right":
            canvas.draw_image(player, (400/2, 400/2), (400,400), (player_pos[0], player_pos[1]), (100, 100))
        else:
            canvas.draw_image(player2, (1200/2, 1200/2), (1200,1200), (player_pos[0], player_pos[1]), (100, 100))        
        canvas.draw_image(shuriken, (130/2, 130/2), (130, 130), (shuriken_pos[0], shuriken_pos[1]), (50,50), shuriken_angle)
        if laser_shot[0] == True:
            canvas.draw_image(laser, (660, 500), (1000, 100), (laser_pos[0][0], laser_pos[0][1]), (60, 16), laser_angle[0])
        if laser_shot[1] == True:
            canvas.draw_image(laser, (660, 500), (1000, 100), (laser_pos[1][0], laser_pos[1][1]), (60, 16), laser_angle[1])
        if laser_shot[2] == True:
            canvas.draw_image(laser, (660, 500), (1000, 100), (laser_pos[2][0], laser_pos[2][1]), (60, 16), laser_angle[2])            
        jump_control()
        side_boundaries()
        movement_updates()
        shuriken_control()
        health_control()
        platform_collision(platform1_topleft[0], platform1_topright[0], platform1_topleft[1], platform1_bottomleft[1])
        platform_collision(platform2_topleft[0], platform2_topright[0], platform2_topleft[1], platform2_bottomleft[1])
        platform_collision(platform3_topleft[0], platform3_topright[0], platform3_topleft[1], platform3_bottomleft[1])
        platform_collision(platform4_topleft[0], platform4_topright[0], platform4_topleft[1], platform4_bottomleft[1])
        platform_collision(platform5_topleft[0], platform5_topright[0], platform5_topleft[1], platform5_bottomleft[1])
        platform_collision(platform6_topleft[0], platform6_topright[0], platform6_topleft[1], platform6_bottomleft[1])
        platform_collision(platform7_topleft[0], platform7_topright[0], platform7_topleft[1], platform7_bottomleft[1])
        enemy_control()
        goal_control()
    elif scene == "game_over":
        canvas.draw_text('Game Over', (WIDTH/2-370.5, HEIGHT/2), 160, "Blue")
    elif scene == "win":
        canvas.draw_image(win_background, (480/2, 360/2), (480, 360), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT)) 
        canvas.draw_text('Congratulations', (WIDTH/2-447, HEIGHT/2 - 100), 140, "Blue")
        canvas.draw_text('You Win!', (WIDTH/2-272, HEIGHT/2 + 100), 140, "Blue")    
    elif scene == "scene2":
        canvas.draw_image(background2, (1248/2, 780/2), (1248, 780), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT)) 
        canvas.draw_image(background1, (3480/2, 2400/2), (3480, 2400), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))

def button_handler():
    new_game()
    
def keydown(key): 
    global jump, scene, shuriken_shot, player_direction
    if key == simplegui.KEY_MAP["w"]:
        jump = True
    if key == simplegui.KEY_MAP["d"]:
        player_vel[0] = 4
        player_direction = "right"
    if key == simplegui.KEY_MAP["a"]:
        player_vel[0] = -4
        player_direction = "left"
    if key == simplegui.KEY_MAP["space"] and (scene == "start" or scene == "scene_instructions"):
        scene = "scene1"
    elif key == simplegui.KEY_MAP["space"] and scene != "start" and scene != "scene_instructions":
        shuriken_shot = True
    if key == simplegui.KEY_MAP["i"] and scene == "start":
        scene = "scene_instructions"
        
def keyup(key):
    global jump, start, player_vel
    if key == simplegui.KEY_MAP["d"]:
        player_vel[0] = 0
    if key == simplegui.KEY_MAP["a"]:
        player_vel[0] = 0
        
#imported images
player = simplegui.load_image('http://assets.stickpng.com/thumbs/588a4ccf528ea3cc60d3c4a5.png')
player2 = simplegui.load_image('http://image.prntscr.com/image/01c3d420d2b6406b96dac71361b5bb70.png')
shuriken = simplegui.load_image('https://cdn2.scratch.mit.edu/get_image/gallery/1426830_200x130.png?v=1438373800.37')
enemy = simplegui.load_image('https://noortor.neocities.org/goombagoo.png')
laser = simplegui.load_image('https://placervilledentistry.com/wp-app/wp-content/uploads/2018/03/effective-treatment-for-cold-sores.jpg')
goal = simplegui.load_image('https://vignette.wikia.nocookie.net/sonic/images/3/3b/Goal_Ring_%28Gen%29.png/revision/latest?cb=20160720102804')
start_background = simplegui.load_image('http://i.imgur.com/UPZX7kn.jpg')
instructions_background = simplegui.load_image('https://s-media-cache-ak0.pinimg.com/736x/40/7e/6e/407e6e494d323fbd13af7bd7b7ea8014.jpg')
background1 = simplegui.load_image('http://eskipaper.com/images/cool-snowy-wallpaper-1.jpg')
win_background = simplegui.load_image('https://i.ytimg.com/vi/ZrVpQqJKXjc/hqdefault.jpg')
# create frame
frame = simplegui.create_frame("Game", WIDTH, HEIGHT)
reset_button = frame.add_button('Reset', button_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
# start frame
new_game()
frame.start()
