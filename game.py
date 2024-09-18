import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("跑酷游戏")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 加载角色图像
player_image = pygame.image.load("player.jpg")  # 确保有一个名为player.png的图像文件
player_image = pygame.transform.scale(player_image, (50, 50))

# 角色和地面属性
player_pos = [50, height - 60]
player_speed = 5
gravity = 0.5
jump_height = 15
is_jumping = False
velocity_y = 0

# 障碍物
obstacles = []
obstacle_width = 50
obstacle_height = 50
obstacle_frequency = 1500  # 每1500毫秒生成一个障碍物

# 计时器
pygame.time.set_timer(pygame.USEREVENT, obstacle_frequency)

# 分数
score = 0
font = pygame.font.SysFont("monospace", 35)

# 游戏主循环
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            obstacle_pos = [width, height - 60]
            obstacles.append(obstacle_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        velocity_y = -jump_height

    if is_jumping:
        player_pos[1] += velocity_y
        velocity_y += gravity
        if player_pos[1] >= height - 60:
            player_pos[1] = height - 60
            is_jumping = False

    # 更新障碍物位置
    for obstacle in obstacles:
        obstacle[0] -= player_speed
        if obstacle[0] < -obstacle_width:
            obstacles.remove(obstacle)
            score += 1

    # 碰撞检测
    for obstacle in obstacles:
        if (player_pos[0] < obstacle[0] + obstacle_width and
            player_pos[0] + 50 > obstacle[0] and
            player_pos[1] < obstacle[1] + obstacle_height and
            player_pos[1] + 50 > obstacle[1]):
            print("游戏结束！得分:", score)
            pygame.quit()
            sys.exit()

    # 绘制角色和障碍物
    screen.blit(player_image, (player_pos[0], player_pos[1]))
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    # 显示分数
    score_text = font.render(f"得分: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(300)