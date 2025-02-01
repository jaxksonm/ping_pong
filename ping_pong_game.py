import pygame
# import pygame.joystick


def show_menu():  # function to handle the menu
    # the comment below is some jetbrains thing regarding the global var
    # noinspection PyGlobalUndefined
    global game_mode
    menu_running = True
    while menu_running:

        screen.fill((0, 0, 0))  # menu background color black
        button_bg_color = (100, 100, 100)  # button background color gray
        text_color = (255, 255, 255)  # text color white

        # text boxes
        play_text = font2.render("MULTIPLAYER", True, text_color)
        single_play_text = font2.render("SINGLE PLAYER", True, text_color)
        quit_text = font2.render("QUIT", True, text_color)

        # button positioning
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        single_play_rect = single_play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

        # add padding so that buttons are clickable in a box
        play_bg_rect = play_rect.inflate(20, 10)
        single_play_bg_rect = single_play_rect.inflate(20, 10)
        quit_bg_rect = quit_rect.inflate(20, 10)

        # draw button backgrounds
        pygame.draw.rect(screen, button_bg_color, play_bg_rect, border_radius=5)
        pygame.draw.rect(screen, button_bg_color, single_play_bg_rect, border_radius=5)
        pygame.draw.rect(screen, button_bg_color, quit_bg_rect, border_radius=5)

        # draw text
        screen.blit(play_text, play_rect)
        screen.blit(single_play_text, single_play_rect)
        screen.blit(quit_text, quit_rect)

        # event handling
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()  # quit game
            if events.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # if play is clicked resume game
                if play_bg_rect.collidepoint(mouse_pos):
                    game_mode = 'multiplayer'
                    menu_running = False  # exit menu

                elif single_play_bg_rect.collidepoint(mouse_pos):
                    game_mode = 'singleplayer'
                    menu_running = False

                elif quit_bg_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()


pygame.init()

# dimension vars
WIDTH = 900
HEIGHT = 600

left_score = 0
right_score = 0

clock = pygame.time.Clock()  # game clock

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # window dimension
pygame.display.set_caption('Ping Pong')  # window name

# paddle config
paddle_width = 15
paddle_height = 50

# ball config
ball_size = 15
ball_speed_x = 4
ball_speed_y = 4

# left paddle pos
left_paddle_x = 50
left_paddle_y = HEIGHT // 2 - paddle_height // 2

# right paddle pos
right_paddle_x = WIDTH - 50 - paddle_width
right_paddle_y = HEIGHT // 2 - paddle_height // 2
ball = pygame.Surface((15, 15))

ball.fill((255, 255, 255))  # color the ball

ball_rect = ball.get_rect()

# movement speed
paddle_speed = 10

# fonts
font = pygame.font.SysFont('Arial', 45)  # font for score
font2 = pygame.font.SysFont('Courier', 60, bold=True)  # font for menu
show_menu()

ball_rect.center = (WIDTH // 2, HEIGHT // 2)  # position ball centered at start
# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # left paddle movement (W - S )
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
        left_paddle_y += paddle_speed

    # right paddle movement (up - down arrow keys)
    # noinspection PyUnboundLocalVariable
    if game_mode == 'multiplayer':
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
            right_paddle_y += paddle_speed

    elif game_mode == 'singleplayer':
        # paddle follows the ball
        # divide paddle height by 2 for the center of the paddle pos
        if ball_rect.y > (WIDTH / 8):
            if right_paddle_y + paddle_height / 2 < ball_rect.y and right_paddle_y < HEIGHT - paddle_height:
                right_paddle_y += paddle_speed
            elif right_paddle_y + paddle_height / 2 > ball_rect.y and right_paddle_y > 0:
                right_paddle_y -= paddle_speed

    # pause game
    if keys[pygame.K_SPACE]:
        show_menu()

    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    # collision with top and bottom wall
    if ball_rect.top <= 0 or ball_rect.bottom + ball_size >= HEIGHT:
        ball_speed_y = -ball_speed_y  # invert the direction

    if ball_rect.left <= 0:
        ball_rect.center = (WIDTH // 2, HEIGHT // 2)  # reset ball pos
        ball_speed_x = -ball_speed_x  # reverse ball direction
        left_score += 1  # increment score by 1

    if ball_rect.right >= WIDTH:
        ball_rect.center = (WIDTH // 2, HEIGHT // 2)  # reset ball pos
        ball_speed_x = -ball_speed_x  # reverse ball direction
        right_score += 1  # increment score by 1

    # paddle collisions
    if ball_rect.colliderect(pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height)):
        ball_speed_x = -ball_speed_x

    if ball_rect.colliderect(pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height)):
        ball_speed_x = -ball_speed_x

    # fill the screen green (for now)
    screen.fill((0, 120, 0))
    # draw line down the middle of the screen
    pygame.draw.line(screen, (0, 0, 0), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 3)

    screen.blit(ball, ball_rect)  # draw ball
    # draw paddles
    pygame.draw.rect(screen, (255, 255, 255),
                     (left_paddle_x, left_paddle_y, paddle_width, paddle_height))  # left paddle
    pygame.draw.rect(screen, (255, 255, 255),
                     (right_paddle_x, right_paddle_y, paddle_width, paddle_height))  # right paddle

    # score board display
    text = font.render(f"{left_score}", True, (255, 255, 255))
    text2 = font.render(f"{right_score}", True, (255, 255, 255))

    # set the texts opposite of each other
    screen.blit(text, (HEIGHT * 2 - WIDTH / 2, 0))
    screen.blit(text2, (WIDTH / 6, 0))

    pygame.display.update()

    # game tick
    clock.tick(60)

pygame.quit()
