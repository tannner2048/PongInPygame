import pygame
import math
#import random


PDHEIGHT = 100
PDWIDTH = 10
PD_SPEED = 280
BALL_SPEED = 320
BALL_RADIUS = 10


def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))

def calc_key(keys_pressed, up, down):
    if keys_pressed[up] and keys_pressed[down]:
        return 0
    if keys_pressed[up]:
        return 1
    if keys_pressed[down]:
        return -1
    return 0

def update_player_pos(paddle_pos, dir, screen, dt):
    if dir == 1:
        new_paddle_pos = paddle_pos - PD_SPEED * dt
    elif dir == -1:
        new_paddle_pos = paddle_pos + PD_SPEED * dt
    else:
        new_paddle_pos = paddle_pos
    
    return clamp(new_paddle_pos, 0 + PDHEIGHT/2, screen.get_height() - PDHEIGHT/2)

def if_ball_collide(rball, rpd1, rpd2, screen_height):
    out_bounds = rball.y < 0 or rball.y > screen_height - BALL_RADIUS*2
    return out_bounds or rball.colliderect(rpd1) or rball.colliderect(rpd2)

def if_point_scored(ball_pos, screen_width):
    if ball_pos.x > screen_width:
        return 1
    if ball_pos.x < 0:
        return -1
    return 0
    
def update_ball_pos(ball_pos, dir, speed, dt):
    return ball_pos + dir * (speed*dt)

def main_loop(screen, clock, dir):
    CENTER = pygame.math.Vector2(screen.get_width()/2, screen.get_height()/2)
    running = True
    dt = 0
    paddle_pos = screen.get_height()/2
    other_paddle_pos = screen.get_height()/2
    ball_pos = CENTER
    font = pygame.font.SysFont('Comic Sans MS', 30)
    collisions = 0
    points1 = 0
    points2 = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black")
        #rects
        rpd1 = pygame.Rect(PDWIDTH, paddle_pos - PDHEIGHT/2, PDWIDTH, PDHEIGHT)
        rpd2 = pygame.Rect(screen.get_width()-PDWIDTH*2, other_paddle_pos - PDHEIGHT/2, PDWIDTH, PDHEIGHT)
        rball = pygame.Rect(ball_pos.x-BALL_RADIUS, ball_pos.y-BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
        pygame.draw.circle(screen, "white", ball_pos, BALL_RADIUS)
        #physics
        keys = pygame.key.get_pressed()
        other_paddle_pos = update_player_pos(other_paddle_pos, calc_key(keys, pygame.K_UP, pygame.K_DOWN), screen, dt)
        paddle_pos = update_player_pos(paddle_pos, calc_key(keys, pygame.K_w, pygame.K_s), screen, dt)
        
        collide = if_ball_collide(rball, rpd1, rpd2, screen.get_height())
        if collide:
            dir = dir.rotate(90)
            collisions += 1
        ball_pos = update_ball_pos(ball_pos, dir, max(BALL_SPEED + (BALL_SPEED/1.5) * math.log10(collisions+1), BALL_SPEED), dt)
        point = if_point_scored(ball_pos, screen.get_width())
        
        if point == 1:
            points1 += 1
            ball_pos = CENTER
            collisions = 0
            dir = -dir
        elif point == -1:
            points2 += 1
            collisions = 0
            ball_pos = CENTER
            dir = -dir
        
        #draw
        pygame.draw.rect(screen, "white", rpd1)
        pygame.draw.rect(screen, "white", rpd2)
        pygame.draw.circle(screen, "white", ball_pos, BALL_RADIUS)
        text_surface = font.render(f"{str(points1)} | {str(points2)}", False, "white")
        screen.blit(text_surface, (screen.get_width()/2 - 25,0))
        
        pygame.display.flip()
        dt = clock.tick(360) / 1000
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    main_loop(pygame.display.set_mode((1280, 720)), pygame.time.Clock(), pygame.Vector2(-1, -1).normalize())

