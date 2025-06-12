import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 300
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game - 난이도 증가 버전")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 공룡 클래스
class Dino:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = 50
        self.y = HEIGHT - self.height - 20
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_force = -12
        self.is_jumping = False

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        if self.y >= HEIGHT - self.height - 20:
            self.y = HEIGHT - self.height - 20
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_force
            self.is_jumping = True

    def draw(self):
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height))

# 장애물 클래스
class Obstacle:
    def __init__(self, speed):
        self.width = 20
        self.height = random.randint(30, 50)
        self.x = WIDTH
        self.y = HEIGHT - self.height - 20
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.x + self.width < 0

    def collide(self, dino):
        dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
        obs_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return dino_rect.colliderect(obs_rect)

# 게임 루프
def main():
    clock = pygame.time.Clock()
    dino = Dino()
    obstacles = []
    score = 0
    font = pygame.font.SysFont(None, 36)
    frame_count = 0
    base_speed = 7  # 시작 속도
    running = True

    while running:
        clock.tick(30)
        win.fill(WHITE)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            dino.jump()

        # 난이도 증가 로직: 시간 지날수록 속도 증가
        difficulty_factor = frame_count // 600  # 600프레임 = 20초
        current_speed = base_speed + difficulty_factor

        # 업데이트
        dino.update()
        dino.draw()

        # 장애물 생성
        if frame_count % 90 == 0:
            obstacles.append(Obstacle(current_speed))

        for obs in list(obstacles):
            obs.update()
            obs.draw()
            if obs.collide(dino):
                running = False
            if obs.off_screen():
                obstacles.remove(obs)
                score += 1

        # 땅 그리기
        pygame.draw.line(win, BLACK, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 2)

        # 점수 표시
        text = font.render(f"Score: {score}", True, BLACK)
        win.blit(text, (10, 10))

        pygame.display.update()
        frame_count += 1

    # 게임 오버 화면
    game_over_screen(score)

def game_over_screen(score):
    win.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, BLACK)
    win.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 24))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
