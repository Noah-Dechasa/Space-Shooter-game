import pgzrun

import random

import sys


#defining actors and starting pos
TITLE = 'ALIEN ASSASSISN!!!'
WIDTH = 800
HEIGHT = 800


game = Actor('m_menu')
game.midtop = (0,800)
game.state = ['title', 'game', 'winner', 'loser', 'about', 'level_2']
game.current_state = game.state[0]


astro = Actor('astro')
astro.pos = (250,250)

alien = Actor('alien')
alien.score = 0

player = Actor('blaster')
player.pos = (WIDTH // 2, HEIGHT - 100)
player.score = 0





lasers = []
aliens = []
astros = []



#drawing everything 
def draw_background():
    for x in range(0, 800, 800):
        for y in range(0, 800, 800):
            screen.blit('start_background', (x, y))           

def draw_start_button():
    game.draw()
    screen.blit('s_start', (250, 600))
     
def draw_game_background():
    for x in range(0, 800, 800):
        for y in range(0, 800, 800):
            screen.blit('moon', (x, y))
    

def draw_game_winner():
    for x in range(0, 800, 800):
        for y in range(0, 800, 800):
            screen.blit('winner', (x, y))
            
def draw_game_loser():
    for x in range(0, 800, 800):
        for y in range(0, 800, 800):
            screen.blit('end_screen-1.png', (x, y))
            
def draw_about_page():
    for x in range(0, 800, 800):
        for y in range(0, 800, 800):
            screen.blit('about_page', (x, y))
            
def draw_level_2():
    for x in range(0, 800, 800):
        for y in range(0, 800, 800):
            screen.blit('level_2', (x, y))
            
def draw_about_button():
    game.draw()
    screen.blit('press_a', (200, 650))
    
def draw_menu_button():
    game.draw()
    screen.blit('m_menu', (250, 700))
            
def draw_lasers():
    global lasers
    for laser in lasers:
        laser.draw()

def draw_aliens():
    global aliens
    for alien in aliens:
        alien.draw()
        
def draw_astros():
    global astros
    for astro in astros:
        astro.draw()

#calling the drawings 
def draw():

    draw_background()
    
    if game.current_state == 'title':
        draw_background()
        draw_start_button()
        draw_about_button()
        draw_menu_button()
    
    elif game.current_state == 'game':
        draw_game_background()
        screen.draw.text("Score: " + str(player.score), bottomright=(WIDTH-10, HEIGHT-5))
        #screen.draw.text("Damages Sustained: " + str(alien.score), bottomright=(200, HEIGHT-5))
        #screen.draw.text("Damages Sustained: " + str(game.score), bottomleft=(10, HEIGHT-5))
        draw_astros()
        draw_lasers()
        player.draw()
        draw_aliens()
        
        
    elif game.current_state == 'loser':
        draw_game_loser()
        
    elif game.current_state == 'winner':
        draw_game_winner()
        
    elif game.current_state == 'about':
        draw_about_page()
        
    elif game.current_state == 'level_2':
        draw_level_2()
        screen.draw.text("Score: " + str(player.score), bottomright=(WIDTH-10, HEIGHT-5))
        #screen.draw.text("Damages Sustained: " + str(alien.score), bottomright=(200, HEIGHT-5))
        draw_astros()
        draw_lasers()
        player.draw()
        draw_aliens()
        

#moving the player
def check_keys(dt):
    if game.current_state == 'game':
        if keyboard.a:
            player.x -= dt * 300
            if player.left < 0:
                player.left = 0
        if keyboard.d:
            player.x += dt * 300
            if player.right > WIDTH:
                player.right = WIDTH
        if keyboard.w:
            player.y -= dt * 200
            if player.y < 0:
                player.y = 0
        if keyboard.s:
            player.y += dt * 200
            if player.y > HEIGHT:
                player.y = HEIGHT

def check_keys_2(dt):
    if game.current_state == 'level_2':
        if keyboard.a:
            player.x -= dt * 300
            if player.left < 0:
                player.left = 0
        if keyboard.d:
            player.x += dt * 300
            if player.right > WIDTH:
                player.right = WIDTH
        if keyboard.w:
            player.y -= dt * 200
            if player.y < 0:
                player.y = 0
        if keyboard.s:
            player.y += dt * 200
            if player.y > HEIGHT:
                player.y = HEIGHT

    

#moving everything else
def move_lasers(dt):
    global lasers
    for laser in lasers:
        laser.y -= dt * 400

def move_aliens(dt):
    global aliens
    for alien in aliens:
        alien.y += dt * 100
        
def move_astros(dt):
    global astros
    for astro in astros:
        astro.x += dt * 100
        
def move_aliens_l2(dt):
    global aliens
    if game.current_state == [5]:
        for alien in aliens:
            alien.y += dt * 300
        
def move_astros_l2(dt):
    global astros
    if game.current_state == [5]:
        for astro in astros:
            astro.y += dt * 300
        

#checking collisions
def check_laser_collisions():
    global lasers
    global aliens
    
    for laser in lasers:

        for alien in aliens:
            
            if laser.colliderect(alien):
                laser.render = False
                alien.render = False
                alien.alive = False

                #screen.blit('boom', (alien.x,alien.y))
                player.score+=1
    
                #clock.schedule_interval(delete_aliens, 3)
                
                
                sounds.explode.play()
                clean_up()

def check_player_collisions():
    global aliens
    global lasers
    global astros
    
    for alien in aliens:
       
        if player.colliderect(alien):
    
            game.current_state = game.state[3]
            
            sounds.explode.play()
           
            clock.unschedule(spawn_alien)
            clock.unschedule(spawn_astros)
            
            aliens = []
            lasers = []
            astros = []
            
            
def check_astro_collisions():
    global astros
    global aliens

    for astro in astros:
        
        for alien in aliens:
    
            if astro.colliderect(alien):
    
                astro.render = False
                astro.alive = False
                alien.render = False
                alien.alive = False
                
                #alien.score += 5
                
                sounds.explode.play()



        
        

      
#cleaning things up     
def clean_up():
    global lasers
    global aliens
    global astros

    
    new_lasers = []
    for laser in lasers:
        if not laser.bottom < 0 and laser.render:
            new_lasers.append(laser)
    lasers = new_lasers
    
    
    new_aliens = []
    for alien in aliens:
        if not alien.top > HEIGHT and alien.render == True:
            new_aliens.append(alien)
    aliens = new_aliens
    
    new_astros = []
    for astro in astros:
        if not astro.top > HEIGHT and astro.render == True:
            new_astros.append(astro)
        astros = new_astros
    



def update(dt):
    check_keys(dt)
    move_lasers(dt)
    move_aliens(dt)
    move_astros(dt)
    check_laser_collisions()
    check_player_collisions()
    check_astro_collisions()
    check_level_2()
    check_keys_2(dt)
    check_winner()
    clean_up()
    move_aliens_l2(dt)
    move_astros_l2(dt)
    
    #check_loser


#spawning everything
def spawn_laser():
    global lasers
    
    laser = Actor('boom')
    
    laser.pos = (player.x, player.y)
    
    laser.render = True
    
    lasers.append(laser)
    
    sounds.laser.play()


def spawn_alien():
    global aliens
    
    alien = Actor('alien')
    
    xpos = random.randint(alien.width, WIDTH - alien.width)
    
    alien.midbottom = (xpos, 0)
    
    alien.render = True
    alien.alive = True

    aliens.append(alien)
    
    
def spawn_astros():
    global astro
    
    astro = Actor('astro')
    
    ypos = random.randint(astro.height, HEIGHT - astro.height)
    
    astro.midbottom = (0, ypos)
    
    astro.render = True
    astro.alive = True
    
    astros.append(astro)
    
    
def check_level_2():
    
    if player.score == 10:
        game.current_state = game.state[5]
        
        
def check_winner():
    
    if player.score == 15:
        game.current_state = game.state[2]
        
        
#def check_loser():
    
    #if player.score ==  15:
        #game.current_state = game.state[3]
    
    

def on_mouse_down(pos):
        spawn_laser()
       
def on_key_down(key):

    if game.current_state == 'title':
        if key == keys.S:
            game.current_state = game.state[1]
            clock.schedule_interval(spawn_alien, 1)
            clock.schedule_interval(spawn_astros, 5)
            
        if key == keys.A:
            game.current_state = game.state[4]
            
    if game.current_state == 'loser':
        if key == keys.M:
            game.current_state = game.state[0]
            
    if game.current_state == 'winner':
        if key == keys.M:
            game.current_state = game.state[0]

    if game.current_state == 'about':
        if key == keys.M:
            game.current_state = game.state[0]
      

            
            
            
pgzrun.go()
