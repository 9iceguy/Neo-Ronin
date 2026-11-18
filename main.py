import math
import random
import sys

import pygame


WIDTH, HEIGHT = 960, 540
FPS = 60
RUN_SECONDS = 75

CYAN = (74, 230, 232)
GOLD = (255, 196, 74)
RED = (236, 82, 92)
GREEN = (98, 220, 145)
WHITE = (245, 245, 238)
INK = (7, 10, 20)
PURPLE = (176, 112, 255)


def load(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, size) if size else image


def sequence(folder, names, size):
    return [load(f"{folder}/{name}", size) for name in names]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("NEO-RONIN: Rift Alchemy")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)
bold = pygame.font.SysFont("consolas", 22, bold=True)
title = pygame.font.SysFont("consolas", 46, bold=True)

backgrounds = [
    load("assets/power-station-tileset/2 Background/Night/1.png", (WIDTH, HEIGHT)),
    load("assets/power-station-tileset/2 Background/Night/2.png", (WIDTH, HEIGHT)),
    load("assets/power-station-tileset/2 Background/Night/3.png", (WIDTH, HEIGHT)),
]
barricade = load("assets/barricade.png", (170, 80))

fighters = {
    "ronin": {
        "name": "JOR",
        "role": "BALANCED",
        "hp": 120,
        "speed": 260,
        "damage": 26,
        "idle": sequence("assets/samurai/Samurai", [f"Idle-{i}.png" for i in range(1, 4)], (105, 105)),
        "run": sequence("assets/samurai/Samurai", [f"Run-{i}.png" for i in range(1, 9)], (105, 105)),
        "attack": sequence("assets/samurai/Samurai", [f"Attack_1-{i}.png" for i in range(1, 5)], (105, 105)),
        "hurt": sequence("assets/samurai/Samurai", [f"Hurt-{i}.png" for i in range(1, 4)], (105, 105)),
    },
    "shinobi": {
        "name": "KIRA",
        "role": "FAST",
        "hp": 95,
        "speed": 330,
        "damage": 21,
        "idle": sequence("assets/shinobi-sprites/Shinobi", ["Idle.png", "Walk.png"], (105, 105)),
        "run": sequence("assets/shinobi-sprites/Shinobi", ["Run.png", "Walk.png"], (105, 105)),
        "attack": sequence("assets/shinobi-sprites/Shinobi", ["Attack_1.png", "Attack_2.png", "Attack_3.png"], (105, 105)),
        "hurt": sequence("assets/shinobi-sprites/Shinobi", ["Hurt.png", "Idle.png"], (105, 105)),
    },
    "cyborg": {
        "name": "NYX",
        "role": "HEAVY",
        "hp": 145,
        "speed": 220,
        "damage": 31,
        "idle": sequence("assets/cyberpunk-characters/3 Cyborg", ["Cyborg_idle.png", "Cyborg_hurt.png"], (105, 105)),
        "run": sequence("assets/cyberpunk-characters/3 Cyborg", ["Cyborg_run.png", "Cyborg_run_attack.png"], (105, 105)),
        "attack": sequence("assets/cyberpunk-characters/3 Cyborg", ["Cyborg_attack1.png", "Cyborg_attack2.png", "Cyborg_punch.png"], (105, 105)),
        "hurt": sequence("assets/cyberpunk-characters/3 Cyborg", ["Cyborg_hurt.png", "Cyborg_idle.png"], (105, 105)),
    },
}

dog_kuro = {
    "idle": sequence("assets/animal/1 Dog", ["Idle.png", "Walk.png"], (72, 72)),
    "attack": sequence("assets/animal/1 Dog", ["Attack.png", "Walk.png"], (72, 72)),
}
dog_shiro = {
    "idle": sequence("assets/animal/2 Dog 2", ["Idle.png", "Walk.png"], (72, 72)),
    "attack": sequence("assets/animal/2 Dog 2", ["Attack.png", "Walk.png"], (72, 72)),
}

enemy_assets = {
    "soldier": (
        sequence("assets/soldier/Soldier_1", [f"Run-right-{i}.png" for i in range(1, 9)], (92, 92)),
        sequence("assets/soldier/Soldier_1", ["Idle-1.png", "Idle-2.png", "Idle-3.png"], (92, 92)),
    ),
    "spirit": (
        sequence("assets/fantasy-enemies/Fire_Spirit", ["Run.png", "Walk.png", "Flame.png"], (82, 82)),
        sequence("assets/fantasy-enemies/Fire_Spirit", ["Idle.png", "Idle_2.png"], (82, 82)),
    ),
    "skeleton": (
        sequence("assets/fantasy-enemies/Skeleton", ["Run.png", "Walk.png"], (90, 90)),
        sequence("assets/fantasy-enemies/Skeleton", ["Idle.png", "Hurt.png"], (90, 90)),
    ),
    "drone": (
        sequence("assets/drones/1 Drones/3", ["Forward.png", "Idle.png", "Fire1.png"], (72, 72)),
        sequence("assets/drones/1 Drones/3", ["Idle.png", "Back.png"], (72, 72)),
    ),
    "boss": (
        sequence("assets/werewolf/Red_Werewolf", ["Run.png", "Run+Attack.png", "Walk.png"], (170, 170)),
        sequence("assets/werewolf/Red_Werewolf", ["Idle.png", "Attack_1.png", "Attack_2.png"], (170, 170)),
    ),
}
slash_frames = sequence("assets/slash/PNG/7", [f"{i}.png" for i in range(1, 11)], (150, 150))


def draw_text(value, pos, color=WHITE, font_obj=font, center=False):
    surface = font_obj.render(str(value), True, color)
    rect = surface.get_rect(topleft=pos)
    if center:
        rect.center = pos
    screen.blit(surface, rect)


def draw_bar(x, y, w, hp, maximum, color):
    pygame.draw.rect(screen, (44, 48, 62), (x, y, w, 9), border_radius=5)
    ratio = max(0, min(1, hp / maximum))
    pygame.draw.rect(screen, color, (x, y, int(w * ratio), 9), border_radius=5)


def draw_button(rect, label, accent=CYAN):
    pygame.draw.rect(screen, (20, 57, 66), rect, border_radius=10)
    pygame.draw.rect(screen, accent, rect, 2, border_radius=10)
    draw_text(label, rect.center, WHITE, bold, True)


def draw_fighter(image, x, y, facing=1, alpha=255):
    if facing < 0:
        image = pygame.transform.flip(image, True, False)
    if alpha != 255:
        image = image.copy()
        image.set_alpha(alpha)
    screen.blit(image, image.get_rect(center=(int(x), int(y))))


class Fighter:
    def __init__(self, kind):
        data = fighters[kind]
        self.kind = kind
        self.x = 180
        self.y = 390
        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.speed = data["speed"]
        self.damage = data["damage"]
        self.facing = 1
        self.anim = 0
        self.attack = 0
        self.hurt = 0
        self.attack_cooldown = 0


class Enemy:
    def __init__(self, kind, level, boss=False):
        self.kind = kind
        self.boss = boss
        side = random.choice((-1, 1))
        self.x = random.randint(710, 900) if side > 0 else random.randint(60, 210)
        self.y = random.randint(320, 465)
        stats = {
            "soldier": (48, 1.15),
            "spirit": (34, 1.45),
            "skeleton": (42, 1.25),
            "drone": (30, 1.7),
            "boss": (420, 1.1),
        }
        hp, speed = stats[kind]
        self.hp = hp + level * (20 if boss else 4)
        self.max_hp = self.hp
        self.speed = speed
        self.anim = random.random() * 4
        self.facing = 1
        self.hit_flash = 0
        self.attack_cooldown = random.uniform(0.2, 1)

    def rect(self):
        size = 125 if self.boss else 72
        return pygame.Rect(int(self.x - size / 2), int(self.y - size / 2), size, size)

    def update(self, px, py, dt):
        dx, dy = px - self.x, py - self.y
        distance = max(1, math.hypot(dx, dy))
        if distance > (80 if self.boss else 50):
            self.x += dx / distance * self.speed * 60 * dt
            self.y += dy / distance * self.speed * 60 * dt
        self.facing = 1 if dx >= 0 else -1
        self.anim += dt * (8 if self.kind != "boss" else 5)
        self.hit_flash -= dt
        self.attack_cooldown -= dt

    def image(self):
        running, idle = enemy_assets[self.kind]
        pool = running if 0.45 < (self.anim % 2) else idle
        return pool[int(self.anim) % len(pool)]


def character_screen():
    selected = "ronin"
    cards = [
        ("ronin", pygame.Rect(80, 170, 240, 250)),
        ("shinobi", pygame.Rect(360, 170, 240, 250)),
        ("cyborg", pygame.Rect(640, 170, 240, 250)),
    ]
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_LEFT):
                    selected = "ronin"
                elif event.key in (pygame.K_2, pygame.K_UP):
                    selected = "shinobi"
                elif event.key in (pygame.K_3, pygame.K_RIGHT):
                    selected = "cyborg"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return selected
            if event.type == pygame.MOUSEBUTTONDOWN:
                for kind, rect in cards:
                    if rect.collidepoint(event.pos):
                        if selected == kind:
                            return kind
                        selected = kind

        screen.blit(backgrounds[0], (0, 0))
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 7, 16, 205))
        screen.blit(shade, (0, 0))
        draw_text("CHOOSE YOUR RUNNER", (480, 60), CYAN, title, True)
        draw_text("NEO-EDO, YEAR 2099", (480, 115), GOLD, bold, True)

        for kind, rect in cards:
            data = fighters[kind]
            accent = GOLD if kind == selected else (70, 82, 96)
            pygame.draw.rect(screen, (17, 26, 38), rect, border_radius=14)
            pygame.draw.rect(screen, accent, rect, 3, border_radius=14)
            frame = data["idle"][int(pygame.time.get_ticks() / 180) % len(data["idle"])]
            draw_fighter(frame, rect.centerx, rect.y + 105)
            draw_text(data["name"], (rect.centerx, rect.y + 160), WHITE, bold, True)
            draw_text(data["role"], (rect.centerx, rect.y + 188), CYAN, font, True)
            draw_text(f"HP {data['hp']}  DMG {data['damage']}", (rect.centerx, rect.y + 218), GOLD, font, True)

        draw_button(pygame.Rect(355, 460, 250, 55), "ENTER THE RIFT")
        pygame.display.update()


def opening(selected):
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(355, 445, 250, 55).collidepoint(event.pos):
                    return True

        screen.blit(backgrounds[1], (0, 0))
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 7, 16, 175))
        screen.blit(shade, (0, 0))
        draw_text("NEO-RONIN", (480, 85), CYAN, title, True)
        draw_text("RIFT ALCHEMY", (480, 140), GOLD, bold, True)
        draw_text("Cyrus broke reality.", (480, 205), WHITE, font, True)
        draw_text("Close the Rift before Kane turns Neo-Edo to gold.", (480, 235), WHITE, bold, True)
        draw_text("MOVE A/D", (250, 310), CYAN, bold, True)
        draw_text("ATTACK J", (480, 310), CYAN, bold, True)
        draw_text("SWITCH DOG T", (710, 310), CYAN, bold, True)
        draw_text("75-second run • collect shards • defeat Kane", (480, 365), GOLD, font, True)
        draw_button(pygame.Rect(355, 445, 250, 55), "BEGIN RUN")
        pygame.display.update()


def game_loop(selected):
    player = Fighter(selected)
    enemies = []
    shards = []
    effects = []
    score = 0
    combo = 0
    elapsed = 0
    spawn = 0
    boss_spawned = False
    boss_cleared = False
    active_dog = "kuro"
    dog_timer = 0
    shiro_used = False
    invulnerable = 0
    result = None
    background_index = 0

    attack_button = pygame.Rect(WIDTH - 170, HEIGHT - 92, 68, 68)
    dog_button = pygame.Rect(WIDTH - 92, HEIGHT - 92, 68, 68)

    while True:
        dt = min(0.033, clock.tick(FPS) / 1000)
        elapsed += dt
        spawn -= dt
        player.attack -= dt
        player.attack_cooldown -= dt
        player.hurt -= dt
        dog_timer -= dt
        invulnerable -= dt
        combo = max(0, combo - dt * 0.35)
        background_index = min(2, int(elapsed // 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_j, pygame.K_x, pygame.K_k):
                    if player.attack_cooldown <= 0:
                        player.attack = 0.25
                        player.attack_cooldown = 0.42 if selected == "shinobi" else 0.55
                if event.key == pygame.K_t:
                    active_dog = "shiro" if active_dog == "kuro" else "kuro"
                    dog_timer = 1.0
                    if active_dog == "shiro" and not shiro_used:
                        player.hp = min(player.max_hp, player.hp + 35)
                        shiro_used = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if attack_button.collidepoint(event.pos) and player.attack_cooldown <= 0:
                    player.attack = 0.25
                    player.attack_cooldown = 0.42 if selected == "shinobi" else 0.55
                elif dog_button.collidepoint(event.pos):
                    active_dog = "shiro" if active_dog == "kuro" else "kuro"
                    dog_timer = 1.0
                    if active_dog == "shiro" and not shiro_used:
                        player.hp = min(player.max_hp, player.hp + 35)
                        shiro_used = True

        keys = pygame.key.get_pressed()
        move = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        if move:
            player.x = max(55, min(WIDTH - 55, player.x + move * player.speed * dt))
            player.facing = move
        if elapsed >= 74:
            if not boss_spawned:
                enemies = [Enemy("boss", int(elapsed // 20), True)]
                boss_spawned = True
                effects.append([player.x, player.y, 0.8, "rift"])
        elif not boss_spawned and spawn <= 0 and len(enemies) < 6:
            roll = random.random()
            kind = "soldier" if roll < 0.38 else "spirit" if roll < 0.68 else "skeleton" if roll < 0.88 else "drone"
            enemies.append(Enemy(kind, int(elapsed // 18)))
            spawn = random.uniform(0.55, 1.05)

        for enemy in enemies:
            enemy.update(player.x, player.y, dt)
            if enemy.rect().colliderect(pygame.Rect(player.x - 38, player.y - 42, 76, 84)):
                if enemy.attack_cooldown <= 0 and invulnerable <= 0:
                    damage = 18 if enemy.boss else 7
                    player.hp -= damage
                    player.hurt = 0.32
                    invulnerable = 0.75
                    enemy.attack_cooldown = 1.2 if enemy.boss else 0.9

        if player.attack > 0:
            attack_rect = pygame.Rect(
                int(player.x + player.facing * 40 - 58),
                int(player.y - 58),
                116,
                116,
            )
            effects.append([player.x + player.facing * 65, player.y, 0.22, "slash"])
            for enemy in enemies[:]:
                if enemy.rect().colliderect(attack_rect) and enemy.hit_flash <= 0:
                    damage = player.damage
                    if selected == "shinobi":
                        damage += 5
                    enemy.hp -= damage
                    enemy.hit_flash = 0.12
                    combo += 0.25
                    if enemy.hp <= 0:
                        score += 100 if enemy.boss else 10
                        if enemy.boss:
                            boss_cleared = True
                        for _ in range(3 if enemy.boss else 2):
                            shards.append([enemy.x + random.randint(-35, 35), enemy.y + random.randint(-20, 20), 9])
                        enemies.remove(enemy)

        if active_dog == "kuro" and dog_timer > 0:
            for enemy in enemies[:]:
                if math.hypot(enemy.x - player.x, enemy.y - player.y) < 125:
                    enemy.hp -= player.damage * 0.32
                    if enemy.hp <= 0:
                        score += 10
                        enemies.remove(enemy)

        for shard in shards[:]:
            dx, dy = player.x - shard[0], player.y - shard[1]
            distance = max(1, math.hypot(dx, dy))
            if distance < 95:
                shard[0] += dx / distance * 7
                shard[1] += dy / distance * 7
            if distance < 38:
                score += 5
                combo += 0.1
                shards.remove(shard)

        effects = [effect for effect in effects if effect[2] > 0]
        for effect in effects:
            effect[2] -= dt

        if player.hp <= 0:
            result = "lose"
        if boss_cleared:
            result = "win"
        if elapsed >= RUN_SECONDS and not boss_spawned:
            result = "win"

        screen.blit(backgrounds[background_index], (0, 0))
        screen.blit(barricade, (665, 430))

        for shard in shards:
            pygame.draw.circle(screen, GOLD, (int(shard[0]), int(shard[1])), shard[2])
            pygame.draw.circle(screen, WHITE, (int(shard[0]), int(shard[1])), 3)

        for effect in effects:
            x, y, life, kind = effect
            if kind == "slash":
                frame = slash_frames[min(len(slash_frames) - 1, int((0.22 - life) * 45))]
                draw_fighter(frame, x, y, player.facing)
            elif kind == "rift":
                pygame.draw.circle(screen, PURPLE, (WIDTH // 2, 390), int(110 * life), 3)

        for enemy in enemies:
            draw_fighter(enemy.image(), enemy.x, enemy.y, enemy.facing)
            draw_bar(enemy.x - 42, enemy.y - 72, 84, enemy.hp, enemy.max_hp, RED)

        data = fighters[selected]
        if player.attack > 0:
            player_frame = data["attack"][int(player.anim) % len(data["attack"])]
        elif player.hurt > 0:
            player_frame = data["hurt"][int(player.anim) % len(data["hurt"])]
        elif move:
            player_frame = data["run"][int(player.anim) % len(data["run"])]
        else:
            player_frame = data["idle"][int(player.anim) % len(data["idle"])]
        player.anim += dt * 10
        draw_fighter(player_frame, player.x, player.y, player.facing)

        dog = dog_kuro if active_dog == "kuro" else dog_shiro
        dog_frame = dog["attack"][int(player.anim) % len(dog["attack"])] if dog_timer > 0 else dog["idle"][int(player.anim) % len(dog["idle"])]
        draw_fighter(dog_frame, player.x - player.facing * 72, player.y + 28, player.facing)

        draw_bar(24, 22, 220, player.hp, player.max_hp, GREEN)
        draw_text(f"HP {max(0, int(player.hp))}", (28, 38), WHITE)
        draw_text(f"SHARDS {score}", (28, 62), GOLD)
        draw_text(f"DOG {active_dog.upper()} {'+' if shiro_used else ''}", (28, 86), CYAN)
        draw_text(f"RIFT {max(0, int(RUN_SECONDS - elapsed))}s", (790, 22), CYAN)
        if combo >= 1:
            draw_text(f"CHAIN x{int(combo)}", (800, 55), GOLD)

        draw_button(attack_button, "J")
        draw_button(dog_button, "DOG", GOLD)

        if result:
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((4, 7, 16, 205))
            screen.blit(shade, (0, 0))
            if result == "win":
                draw_text("THE RIFT IS STABLE", (480, 190), CYAN, title, True)
                draw_text("Cyrus's signal fades beneath Kane's armor.", (480, 250), WHITE, bold, True)
            else:
                draw_text("THE RIFT WON THIS RUN", (480, 190), RED, title, True)
                draw_text("Kane grows stronger. Jor will try again.", (480, 250), WHITE, bold, True)
            draw_text(f"Alchemy Shards {score}", (480, 305), GOLD, title, True)
            draw_button(pygame.Rect(330, 390, 300, 60), "RUN AGAIN")
            pygame.display.update()
            while True:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit"
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return "again"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.Rect(330, 390, 300, 60).collidepoint(event.pos):
                            return "again"

        pygame.display.update()


def main():
    while True:
        selected = character_screen()
        if selected is None:
            break
        if not opening(selected):
            break
        result = game_loop(selected)
        if result != "again":
            break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
