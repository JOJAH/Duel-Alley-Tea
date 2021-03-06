import pygame
from testbase import config, make_shops, event_checks
from pygame import K_DOWN, K_LCTRL, K_LEFT, K_RCTRL, K_RIGHT, K_UP, KEYDOWN, KEYUP, QUIT, K_a, K_d, K_s, K_w, mixer
from pygame.locals import (
    K_ESCAPE
)

app_start = False

mixer.init()

channel1 = pygame.mixer.Channel(0)

mixer.music.load('Sounds\\Fight-o.mp3')

# rat_noise = mixer.Sound('Sounds\\pests_2.wav')
# rat_noise_left = mixer.Sound('Sounds\\pests_1.wav')

mixer.music.set_volume(0.8)

# play_rats = True
mixer.music.play(-1)

FPS = 60
SPEED = 8
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

walk_count_left = 0
walk_count_right = 0
rat_count_left = 0
rat_count_right = 0
customer_left_count = 0
customer_right_count = 0
leak_count = 0

class Sink(pygame.sprite.Sprite):
    def __init__(self):
        super(Sink, self).__init__()
        self.surf = pygame.Surface((5, 100), pygame.SRCALPHA)
        self.rect_left = self.surf.get_rect()
        self.rect_left.move_ip(5, 500)
        self.rect_right = self.surf.get_rect()
        self.rect_right.move_ip(1275, 500)
        leak_transform = (200, 130)
        leaking_1 = pygame.transform.scale(pygame.image.load("Images\\leaking-1.png"), leak_transform)
        leaking_2 = pygame.transform.scale(pygame.image.load("Images\\leaking-2.png"), leak_transform)
        leaking_1_left = pygame.transform.scale(pygame.image.load("Images\\leaking-1-left.png"), leak_transform)
        leaking_2_left = pygame.transform.scale(pygame.image.load("Images\\leaking-2-left.png"), leak_transform)
        self.leaking = [leaking_1, leaking_2, leaking_1, leaking_2, leaking_1, leaking_2, leaking_1, leaking_2]
        self.leaking_left = [leaking_1_left, leaking_2_left, leaking_1_left, leaking_2_left, leaking_1_left, leaking_2_left, leaking_1_left, leaking_2_left]
        self.leaking_rect_left = leaking_1_left.get_rect()
        self.leaking_rect_right = leaking_1_left.get_rect()
        self.leaking_rect_left.move_ip(-70, 520)
        self.leaking_rect_right.move_ip(1155, 520)

    def draw(self, surface):
        surface.blit(self.surf, self.rect_left)
        surface.blit(self.surf, self.rect_right)

    def leak_right(self, surface):
        global leak_count
        if leak_count + 1 >= FPS:
            leak_count = 0
        surface.blit(self.leaking[int(leak_count//7.5)], self.leaking_rect_right)
        leak_count += 1

    
    def leak_left(self, surface):
        global leak_count
        if leak_count + 1 >= FPS:
            leak_count = 0
        surface.blit(self.leaking_left[int(leak_count//7.5)], self.leaking_rect_left)
        leak_count += 1


class Phone(pygame.sprite.Sprite):
    def __init__(self):
        super(Phone, self).__init__()
        self.surf = pygame.Surface((2, 100), pygame.SRCALPHA)
        self.rect_left = self.surf.get_rect()
        self.rect_left.move_ip(249, 474)
        self.rect_right = self.surf.get_rect()
        self.rect_right.move_ip(1028, 474)

    def draw(self, surface):
        surface.blit(self.surf, self.rect_left)
        surface.blit(self.surf, self.rect_right)


class CashRegister():
    def __init__(self):
        super(CashRegister, self).__init__()
        self.surf = pygame.Surface((2, 100), pygame.SRCALPHA)
        self.rect_left = self.surf.get_rect()
        self.rect_left.move_ip(483, 474)
        self.rect_right = self.surf.get_rect()
        self.rect_right.move_ip(793, 474)

    def draw(self, surface):
        surface.blit(self.surf, self.rect_left)
        surface.blit(self.surf, self.rect_right)


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super(Floor, self).__init__()
        self.surf_left = pygame.Surface((1280, 10), pygame.SRCALPHA)
        self.rect_left = self.surf_left.get_rect()
        self.rect_left.move_ip(0, 635)
        self.surf_right = pygame.Surface((1280, 10), pygame.SRCALPHA)
        self.rect_right = self.surf_right.get_rect()
        self.rect_right.move_ip(0, 638)

    def draw(self, surface):
        surface.blit(self.surf_left, self.rect_left)
        surface.blit(self.surf_right, self.rect_right)


class Rats(pygame.sprite.Sprite):
    def __init__(self):
        super(Rats, self).__init__()
        rat_1 = pygame.image.load("Images\\rat-1.png")
        rat_2 = pygame.image.load("Images\\rat-2.png")
        rat_1_right = pygame.transform.flip(pygame.image.load("Images\\rat-1.png"), True, False)
        rat_2_right = pygame.transform.flip(pygame.image.load("Images\\rat-2.png"), True, False)
        self.run = [rat_1, rat_2, rat_1, rat_2, rat_1, rat_2, rat_1, rat_2]
        self.run_right = [rat_1_right, rat_2_right, rat_1_right, rat_2_right, rat_1_right, rat_2_right, rat_1_right, rat_2_right]
        self.rect = rat_1.get_rect()
        self.looking = 'right'

    def place_right(self):
        self.rect.move_ip(800,600)

    def place_left(self):
        self.rect.move_ip(500, 600)

    def update_right(self):
        if self.looking == 'left':
            self.rect.move_ip(-8, 0)
        else:
            self.rect.move_ip(8, 0)

    def update_left(self):
        if self.looking == 'left':
            self.rect.move_ip(-8, 0)
        else:
            self.rect.move_ip(8, 0)

    def draw(self, surface):
        global rat_count_right
        if rat_count_right + 1 >= FPS:
            rat_count_right = 0

        if self.looking == 'right':
            surface.blit(self.run[int(rat_count_right//7.5)], self.rect)
            rat_count_right += 1
        else:
            surface.blit(self.run_right[int(rat_count_right//7.5)], self.rect)
            rat_count_right += 1


class FrontWall(pygame.sprite.Sprite):
    def __init__(self):
        super(FrontWall, self).__init__()
        self.surf_left = pygame.Surface((10, 720), pygame.SRCALPHA)
        self.rect_left = self.surf_left.get_rect()
        self.rect_left.move_ip(558, 0)
        self.surf_right = pygame.Surface((10, 720), pygame.SRCALPHA)
        self.rect_right = self.surf_right.get_rect()
        self.rect_right.move_ip(710, 0)

    def draw(self, surface):
        surface.blit(self.surf_left, self.rect_left)
        surface.blit(self.surf_right, self.rect_right)


class BackWall(pygame.sprite.Sprite):
    def __init__(self):
        super(BackWall, self).__init__()
        self.surf_left = pygame.Surface((1, 720), pygame.SRCALPHA)
        self.rect_left = self.surf_left.get_rect()
        self.rect_left.move_ip(0, 0)
        self.surf_right = pygame.Surface((10, 720), pygame.SRCALPHA)
        self.rect_right = self.surf_right.get_rect()
        self.rect_right.move_ip(1279, 0)

    def draw(self, surface):
        surface.blit(self.surf_left, self.rect_left)
        surface.blit(self.surf_right, self.rect_right)


class Customer(pygame.sprite.Sprite):
    def __init__(self):
        super(Customer, self).__init__()
        self.transform = (300, 300)
        customer_right_2 = pygame.transform.scale(pygame.image.load("Images\\customer-2.png"), self.transform)
        customer_right_3 = pygame.transform.scale(pygame.image.load("Images\\customer-3.png"), self.transform)
        customer_right_4 = pygame.transform.scale(pygame.image.load("Images\\customer-4.png"), self.transform)
        customer_right_5 = pygame.transform.scale(pygame.image.load("Images\\customer-5.png"), self.transform)
        customer_right_6 = pygame.transform.scale(pygame.image.load("Images\\customer-6.png"), self.transform)
        customer_right_7 = pygame.transform.scale(pygame.image.load("Images\\customer-7.png"), self.transform)
        customer_right_8 = pygame.transform.scale(pygame.image.load("Images\\customer-8.png"), self.transform)
        customer_right_9 = pygame.transform.scale(pygame.image.load("Images\\customer-9.png"), self.transform)
        customer_right_10 = pygame.transform.scale(pygame.image.load("Images\\customer-10.png"), self.transform)

        customer_left_2 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-2.png"), True, False), self.transform)
        customer_left_3 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-3.png"), True, False), self.transform)
        customer_left_4 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-4.png"), True, False), self.transform)
        customer_left_5 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-5.png"), True, False), self.transform)
        customer_left_6 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-6.png"), True, False), self.transform)
        customer_left_7 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-7.png"), True, False), self.transform)
        customer_left_8 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-8.png"), True, False), self.transform)
        customer_left_9 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-9.png"), True, False), self.transform)
        customer_left_10 = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images\\customer-10.png"), True, False), self.transform)

        self.customer_left_wave = [customer_left_2, customer_left_3, customer_left_4, customer_left_5, customer_left_6, customer_left_7, customer_left_8, customer_left_9]
        self.customer_right_wave = [customer_right_2, customer_right_3, customer_right_4, customer_right_5, customer_right_6, customer_right_7, customer_right_8, customer_right_9]
        self.rect = customer_left_2.get_rect()

    def place_left(self):
        self.rect.move_ip(435, 470)

    def place_right(self):
        self.rect.move_ip(530, 440)

    def draw_left(self, surface):
        global customer_left_count

        if customer_left_count + 1 > FPS//2:
            customer_left_count = 0

        surface.blit(self.customer_left_wave[int(customer_left_count//3.75)], self.rect)
        customer_left_count += 1

    def draw_right(self, surface):
        global customer_right_count

        if customer_right_count + 1 > FPS//2:
            customer_right_count = 0

        surface.blit(self.customer_right_wave[int(customer_right_count//3.75)], self.rect)
        customer_right_count += 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.run_index = 0
        self.transform = (120, 120)
        running_1_left = pygame.transform.scale(pygame.image.load("Images\\running-1.png"), self.transform)
        running_1_right = pygame.transform.scale(pygame.image.load("Images\\running-1-right.png"), self.transform)
        running_2_left = pygame.transform.scale(pygame.image.load("Images\\running-2.png"), self.transform)
        running_2_right = pygame.transform.scale(pygame.image.load("Images\\running-2-right.png"), self.transform)
        standing_1_left = pygame.transform.scale(pygame.image.load("Images\\standing-1.png"), self.transform)
        standing_1_right = pygame.transform.scale(pygame.image.load("Images\\standing-1-right.png"), self.transform)
        standing_2_left = pygame.transform.scale(pygame.image.load("Images\\standing-2.png"), self.transform)
        standing_2_right = pygame.transform.scale(pygame.image.load("Images\\standing-2-right.png"), self.transform)
        self.running_left = [running_1_left, running_2_left, running_1_left, running_2_left, running_1_left, running_2_left, running_1_left, running_2_left]
        self.running_right = [running_1_right, running_2_right, running_1_right, running_2_right, running_1_right, running_2_right, running_1_right, running_2_right]
        self.standing_left = [standing_1_left, standing_2_left, standing_1_left, standing_2_left, standing_1_left, standing_2_left, standing_1_left, standing_2_left]
        self.standing_right = [standing_1_right, standing_2_right, standing_1_right, standing_2_right, standing_1_right, standing_2_right, standing_1_right, standing_2_right]
        self.rect = self.standing_left[0].get_rect()
        

    def place_right(self):
        self.rect.move_ip(1180, 500)
        self.last_look = 'left'

    def place_left(self):
        self.rect.move_ip(0, 500)
        self.last_look = 'right'

    def update_left(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            self.rect.move_ip(-SPEED, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(SPEED, 0)

    def update_right(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(SPEED, 0)

    def draw_left(self, surface):
        global walk_count_left
        pressed_keys = pygame.key.get_pressed()
        
        if walk_count_left + 1 >= FPS:
                walk_count_left = 0

        if pressed_keys[K_a]:
            surface.blit(self.running_left[int(walk_count_left//7.5)], self.rect)
            walk_count_left += 1
            self.last_look = 'left'
        elif pressed_keys[K_d]:
            surface.blit(self.running_right[int(walk_count_left//7.5)], self.rect)
            walk_count_left += 1
            self.last_look = 'right'
        else:
            if self.last_look == 'right':
                surface.blit(self.standing_right[int(walk_count_left//7.5)], self.rect)
                walk_count_left += 1
            elif self.last_look == 'left':
                surface.blit(self.standing_left[int(walk_count_left//7.5)], self.rect)
                walk_count_left += 1

    def draw_right(self, surface):
            global walk_count_right
            pressed_keys = pygame.key.get_pressed()
            
            if walk_count_right + 1 >= FPS:
                    walk_count_right = 0

            if pressed_keys[K_LEFT]:
                surface.blit(self.running_left[int(walk_count_right//7.5)], self.rect)
                walk_count_right += 1
                self.last_look = 'left'
            elif pressed_keys[K_RIGHT]:
                surface.blit(self.running_right[int(walk_count_right//7.5)], self.rect)
                walk_count_right += 1
                self.last_look = 'right'
            else:
                if self.last_look == 'right':
                    surface.blit(self.standing_right[int(walk_count_right//7.5)], self.rect)
                    walk_count_right += 1
                elif self.last_look == 'left':
                    surface.blit(self.standing_left[int(walk_count_right//7.5)], self.rect)
                    walk_count_right += 1


if __name__ == '__main__':           
    running = True

    pygame.init()
    pygame.font.init()

    myFont = pygame.font.SysFont("Comc Sans MS", 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    shops = make_shops(config["shops"], config["probabilities"])
    
    customer_animation_counter_right = 0
    customer_animation_counter_left = 0
    player_left = Player()
    player_left.place_left()
    player_right = Player()
    player_right.place_right()
    floor = Floor()
    sink = Sink()
    phone = Phone()
    cashregister = CashRegister()
    front_wall = FrontWall()
    back_wall = BackWall()
    rat_left = Rats()
    rat_left.place_left()
    rat_right = Rats()
    rat_right.place_right()
    customer_left = Customer()
    customer_left.place_left()
    customer_right = Customer()
    customer_right.place_right()
    frame_count = 0

    def check_time():
        global frame_count
        frame_count += 1
        if frame_count + 1 >= FPS:
            event_checks(shops[0])
            event_checks(shops[1])
            frame_count = 0

    pygame.display.update()

    while running:
        if app_start == False:
            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\startscreen.png").convert(), (1280, 720)), (0, 0))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    app_start = True
            pygame.display.update()
            FramePerSec.tick(FPS)

        else:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_DOWN:
                        if sink.rect_right.colliderect(player_right.rect):
                            shops[1].start_cleaning()
                    elif event.key == K_s:
                        if sink.rect_left.colliderect(player_left.rect):
                            shops[0].start_cleaning()
                    elif event.key == K_w:
                        if phone.rect_left.colliderect(player_left.rect):
                            pygame.mixer.Sound.play(mixer.Sound('Sounds\\phone-calls.mp3'))
                            shops[0].call_pest_control()
                    elif event.key == K_UP:
                        if phone.rect_right.colliderect(player_right.rect):
                            pygame.mixer.Sound.play(mixer.Sound('Sounds\\phone-calls.mp3'))
                            shops[1].call_pest_control()
                    elif event.key == K_RCTRL:
                        if sink.rect_right.colliderect(player_right.rect):
                            shops[1].fix_leak()
                    elif event.key == K_LCTRL:
                        if sink.rect_left.colliderect(player_left.rect):
                            shops[0].fix_leak()
                    
                elif event.type == KEYUP:
                    if event.key == K_DOWN:
                        shops[1].stop_cleaning()
                    elif event.key == K_s:
                        shops[0].stop_cleaning()
                elif event.type == QUIT:
                    running = False
            
            check_time()
            screen.fill(BLACK)
            screen.blit(pygame.transform.smoothscale(pygame.image.load("Images\\backgroundtest6.png").convert(), (1280, 720)), (0, 0))
            floor.draw(screen)
            front_wall.draw(screen)
            back_wall.draw(screen)
            sink.draw(screen)
            phone.draw(screen)
            cashregister.draw(screen)
            if shops[1].leaking:
                sink.leak_right(screen)
            if shops[0].leaking:
                sink.leak_left(screen)  
            if shops[0].is_infested:
                rat_left.update_left()
                rat_left.draw(screen)
            if shops[1].is_infested:
                rat_right.update_right()
                rat_right.draw(screen)
            if shops[0].has_customer == True:
                if customer_animation_counter_left + 1 <= FPS//2:
                    customer_left.draw_left(screen)
                    customer_animation_counter_left += 1
                else:
                    customer_animation_counter_left = 0
                    shops[0].has_customer = False

            if shops[1].has_customer == True:
                if customer_animation_counter_right + 1 <= FPS//2:
                    customer_right.draw_right(screen)
                    customer_animation_counter_right += 1
                else:
                    customer_animation_counter_right = 0
                    shops[1].has_customer = False



            screen.blit(pygame.image.load(shops[1].img_file_names["cleanliness_overlay"]), (757, 284))
            screen.blit(pygame.image.load(shops[0].img_file_names["cleanliness_overlay"]), (-263, 284))
            hygiene_rating_1 = pygame.transform.smoothscale(pygame.image.load(shops[1].img_file_names["hygiene_score_image"]), (120, 80))
            screen.blit(hygiene_rating_1, (700, 240))
            hygiene_rating_0 = pygame.transform.smoothscale(pygame.image.load(shops[0].img_file_names["hygiene_score_image"]), (120, 80))
            screen.blit(hygiene_rating_0, (460, 240))
            shop_1_money = myFont.render(f"Moneys: {shops[0].moneys}", False, (0, 0, 0))
            screen.blit(shop_1_money, (10, 230))
            shop_2_money = myFont.render(f"Moneys: {shops[1].moneys}", False, (0, 0, 0))
            screen.blit(shop_2_money, (1133, 230))
            player_left.update_left()
            player_right.update_right()
            
            # Exceptions
            if not floor.rect_left.colliderect(player_left.rect):
                player_left.rect.move_ip(0, 3)
            if not floor.rect_right.colliderect(player_right.rect):
                player_right.rect.move_ip(0, 3)
            if front_wall.rect_left.colliderect(player_left.rect):
                player_left.rect.move_ip(-SPEED, 0)
            if front_wall.rect_right.colliderect(player_right.rect):
                player_right.rect.move_ip(SPEED, 0)
            if back_wall.rect_left.colliderect(player_left.rect):
                player_left.rect.move_ip(SPEED, 0)
            if back_wall.rect_right.colliderect(player_right.rect):
                player_right.rect.move_ip(-SPEED, 0)
            if back_wall.rect_right.colliderect(rat_right.rect):
                rat_right.looking = 'left'
            if back_wall.rect_left.colliderect(rat_left.rect):
                rat_left.looking = 'right'
            if front_wall.rect_left.colliderect(rat_left.rect.inflate(65, 0)):
                rat_left.looking = 'left'
            if front_wall.rect_right.colliderect(rat_right.rect.inflate(65, 0)):
                rat_right.looking = 'right'


            player_left.draw_left(screen)
            player_right.draw_right(screen)

            pygame.display.update()
            FramePerSec.tick(FPS)