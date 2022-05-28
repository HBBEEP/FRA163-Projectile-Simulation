import pygame
import math
from sys import exit
import time
import csv
# ---------------------------------------------------------------------------------------------------------------------#

# >Pygame starts here---------------------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Studio Simulation Project")
clock = pygame.time.Clock()
my_font = pygame.font.Font('font/OpenSans-SemiBold.ttf', 18)
my_font_2 = pygame.font.Font('font/OpenSans-SemiBold.ttf', 24)
COLOR_INACTIVE = pygame.Color('Orange')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
# >---------------------------------------------------------------------------------------------------------------------


# >Import Background & Icon -------------------------------------------------------------------------------------------------

# background
light_mode = pygame.image.load('background/light_mode.png').convert_alpha()
dark_mode = pygame.image.load('background/dark_mode.png').convert_alpha()

light_mode_sim = pygame.image.load("background/light_mode_sim.png").convert_alpha()
dark_mode_sim = pygame.image.load("background/dark_mode_sim.png").convert_alpha()

light_mode_member = pygame.image.load("background/light_mode_member.png").convert_alpha()
dark_mode_member = pygame.image.load("background/dark_mode_member.png").convert_alpha()

# icon
sun_surface = pygame.image.load("icon/sun.png").convert_alpha()
sun_rect = sun_surface.get_rect(midbottom = (126,78))

moon_surface = pygame.image.load("icon/moon.png").convert_alpha()
moon_rect = moon_surface.get_rect(midbottom = (58, 78))

save_surface = pygame.image.load("icon/save.png").convert_alpha()
save_rect = save_surface.get_rect(midbottom = (960, 585))

clear_surface = pygame.image.load("icon/clear.png").convert_alpha()
clear_rect = clear_surface.get_rect(midbottom = (1065, 585))

play_surface = pygame.image.load("icon/play.png").convert_alpha()
play_rect = play_surface.get_rect(midbottom = (1167, 585))


# >---------------------------------------------------------------------------------------------------------------------



# >class ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# >>Class Button--------------------------------------------------------------------------------------------------------

class BoolCheck:
    def __init__(self):
        self.my_bool = False

    def my_bool_return(self):
        return self.my_bool  # False

    def my_change_bool(self, my_change_bool):
        self.my_bool = my_change_bool


class Button:
    def __init__(self, text, width, height, pos, color, font_size = 18):

        self.pressed = False

        self.top_rect = pygame.Rect(pos, (width, height))

        self.font =pygame.font.Font('font/OpenSans-SemiBold.ttf', font_size)

        self.bottom_rect = pygame.Rect(pos, (width, height))

        self.my_color_1 = color
        self.my_color_2 = color

        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.my_color_1, self.top_rect, border_radius=25)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):

        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):

            self.my_color_1 = '#CDDA8F'
            if pygame.mouse.get_pressed()[0] == 1 and self.pressed == False:
                self.my_color_1 = '#CDDA8F'
                self.pressed = True
                return True

        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False
            self.my_color_1 = self.my_color_2


# >Class InputBox-------------------------------------------------------------------------------------------------------
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)

        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = my_font.render(text, True, self.color)
        print(type(self.txt_surface))
        self.active = False


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = my_font.render(self.text, True, self.color)

    def draw(self, Screen):
        Screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(Screen, self.color, self.rect, 2)

    def my_clear(self):
        if clear_bool.my_bool_return():
            self.text = ''
            self.txt_surface = my_font.render(self.text, True, self.color)
            user_input_bool.my_change_bool(False)
            self.active = False
            clear_bool.my_change_bool(False)
            return True


# >---------------------------------------------------------------------------------------------------------------------


# >Class Test_Calculate-------------------------------------------------------------------------------------------------
class MyCalculate:
    def __init__(self, m_3, theta, spring_pull_length, k_constant):
        self.m_1 = 0.180
        self.m_2 = None
        self.m_3 = m_3 / 1000
        self.theta = theta
        self.spring_pull_length = spring_pull_length / 100
        self.k_constant = k_constant
        self.gravity = 9.81
        self.velocity = 0
        self.time = 0

    def only_return_velocity(self):
        self.velocity = ((self.m_1 + self.m_3) / self.m_3) * (
            pow((self.k_constant * self.spring_pull_length * self.spring_pull_length) - (
                    (self.m_1 + self.m_3) * self.gravity * (self.spring_pull_length + 0.08) * (
                math.sin(math.radians(self.theta)))), 0.5))
        return self.velocity

    def only_return_time(self):
        a = (9.81)/2
        b =  self.velocity * math.sin(math.radians(self.theta))*(-1)
        c = -0.40
        dis = (b**2) - (4*a*c)

        root1 = ((-b + math.sqrt(dis) )/ (2 * a))
        # root2 = ((-b - math.sqrt(dis) )/ (2 * a))
        self.time = root1
        return self.time


    def only_return_max_height(self):
        height = (pow(self.velocity * math.sin(math.radians(self.theta)), 2) / (2 * self.gravity)) + 0.40

        return height


# >Class Ball-----------------------------------------------------------------------------------------------------------

class Ball:
    def __init__(self, x, y, v0, theta, timestep, color):
        self.theta = theta
        self.pos = pygame.Vector2()
        self.init_pos = pygame.Vector2(x, y)
        self.init_vel = pygame.Vector2(math.cos(theta * math.pi / 180) * v0, math.sin(theta * math.pi / 180) * v0)
        self.init_accel = pygame.Vector2(0, (-9.81))
        self.my_time = 0
        self.timestep = timestep
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, [(self.pos.x * 150) + 130, 400 - (self.pos.y * 150)], 1)

    def update(self):
        if 0 <= self.pos.y <= 2.2 and self.pos.x <= 4.5:
            self.pos = self.init_pos + self.init_vel * self.my_time + self.init_accel * self.my_time * self.my_time * 0.5
            self.my_time += self.timestep


# >---------------------------------------------------------------------------------------------------------------------


# >Button---------------------------------------------------------------------------------------------------------------
start_button = Button('Start', 250, 100, (515, 552), "#AFA2F9", 32)

member_button = Button('', 40, 40, (1195,645), "#FBEEB7")
back_to_sim_button = Button('', 40, 40, (1136, 645), "#FBEEB7")
save_button = Button('', 75, 79, (921,521), "#FBEEB7")
test_error = Button("Please check : only number/decimal is allowed", 341, 115, (894, 507), "#FF3333", 15)
clear_test = Button('', 75, 79, (1027, 521), "#FBEEB7")
play_test = Button('',75, 79, (1129, 521), "#FBEEB7")

bright_button = Button('', 50, 50, (101,37), "#FBEEB7")
dark_button = Button('', 50, 50, (32, 37), "#B7C4FB")

home_button = Button('',40,40, (1077,645), "#FBEEB7")

ball_mass_error_button = Button('must be in the range 10-200 grams', 246, 39, (662, 127), '#FF3333',11)
launcher_angle_error_button = Button('must be in the range 1-89 degrees', 246, 39, (662, 207), '#FF3333',11)
spring_pull_length_error_button = Button('must be in the range 1-15 cm', 246, 39, (662, 289), '#FF3333',11)
spring_constant_error_button = Button('must be in the range 100-1000 N/m', 246, 39, (662, 371), '#FF3333',11)

# >---------------------------------------------------------------------------------------------------------------------


# >Input Box------------------------------------------------------------------------------------------------------------
input_box1 = InputBox(921, 131, 231, 31)
input_box2 = InputBox(921, 211, 231, 31)
input_box3 = InputBox(921, 293, 231, 31)
input_box4 = InputBox(921, 376, 231, 31)
input_boxes = [input_box1, input_box2, input_box3, input_box4]
# >---------------------------------------------------------------------------------------------------------------------

# >Global Boolean-------------------------------------------------------------------------------------------------------
run = True

user_input_bool = BoolCheck()
clear_bool =  BoolCheck()
save_bool =  BoolCheck()
ball_bool =  BoolCheck()
member_bool =  BoolCheck()
color_bool =  BoolCheck()
color_bool.my_change_bool(True)
start_bool =  BoolCheck()
start_bool.my_change_bool(True)
sim_bool =  BoolCheck()
bright_dark_bool =  BoolCheck()
bright_dark_bool.my_change_bool(True)

error_bool =  BoolCheck()
error_bool_1 = BoolCheck()
error_bool_2 = BoolCheck()
error_bool_3 = BoolCheck()
error_bool_4 = BoolCheck()

# >---------------------------------------------------------------------------------------------------------------------
while run:
    if start_bool.my_bool_return():
        if bright_dark_bool.my_bool_return():
            screen.blit(light_mode, (0,0))
            dark_button.draw()
            if dark_button.check_click():
                bright_dark_bool.my_change_bool(False)
            screen.blit(sun_surface, sun_rect)
            screen.blit(moon_surface, moon_rect)
            start_button.draw()
        else:
            screen.blit(dark_mode, (0,0))
            bright_button.draw()
            if bright_button.check_click():
                bright_dark_bool.my_change_bool(True)
            screen.blit(sun_surface, sun_rect)
            screen.blit(moon_surface, moon_rect)
            start_button.draw()

        if start_button.check_click():
           start_bool.my_change_bool(False)
           sim_bool.my_change_bool(True)
    if sim_bool.my_bool_return():

        if bright_dark_bool.my_bool_return():
            screen.blit(light_mode_sim, (0,0))
        else:
            screen.blit(dark_mode_sim, (0,0))
        for box in input_boxes:
            box.draw(screen)

        # Button
        save_button.draw()
        clear_test.draw()

        member_button.draw()
        home_button.draw()
        play_test.draw()

        screen.blit(save_surface, save_rect)
        screen.blit(clear_surface, clear_rect)
        screen.blit(play_surface, play_rect)
        if home_button.check_click():
            start_bool.my_change_bool(True)
            sim_bool.my_change_bool(False)

        if save_button.check_click():
            save_bool.my_change_bool(True)
        try:
            if save_bool.my_bool_return():
                my_cal = MyCalculate(float(input_boxes[0].text), float(input_boxes[1].text),
                                        float(input_boxes[2].text), float(input_boxes[3].text))

                condition_1 = float(input_boxes[0].text) < 10 or float(input_boxes[0].text)> 200
                condition_2 = float(input_boxes[1].text) < 1 or float(input_boxes[1].text) > 89
                condition_3 = float(input_boxes[2].text) < 1 or float(input_boxes[2].text) > 15
                condition_4 = float(input_boxes[3].text) < 100 or float(input_boxes[3].text) > 1000

                if condition_1:
                    error_bool_1.my_change_bool(True)
                elif condition_2:
                    error_bool_2.my_change_bool(True)
                elif condition_3:
                    error_bool_3.my_change_bool(True)
                elif condition_4:
                    error_bool_4.my_change_bool(True)
                else:
                    error_bool_1.my_change_bool(False)
                    error_bool_2.my_change_bool(False)
                    error_bool_3.my_change_bool(False)
                    error_bool_4.my_change_bool(False)

                    velocity = my_cal.only_return_velocity()
                    velocity = round(velocity, 2)


                    velocity_surf = my_font_2.render(f'{velocity}', False, '#5170F5')
                    velocity_rect = velocity_surf.get_rect(center=(446, 595))

                    time1 = my_cal.only_return_time()
                    time1 = round(time1, 2)

                    time1_surf = my_font_2.render(f'{time1}', False, '#5170F5')
                    time1_rect = time1_surf.get_rect(center=(196, 595))

                    maximum_height = my_cal.only_return_max_height()
                    maximum_height = round(maximum_height, 2)

                    max_h_surf = my_font_2.render(f'{maximum_height}', False, '#5170F5')
                    max_h_rect = max_h_surf.get_rect(center=(712, 595))


                    save_bool.my_change_bool(False)
                    user_input_bool.my_change_bool(True)

                    with open('data.csv', 'a') as f:
                        writer = csv.writer(f)
                        fields = [' ',float(input_boxes[0].text), float(input_boxes[1].text),
                                            float(input_boxes[2].text), float(input_boxes[3].text),'', time1, velocity, maximum_height]
                        writer.writerow(fields)

        except:
            test_error.draw()


        if error_bool_1.my_bool_return():
            ball_mass_error_button.draw()
        if error_bool_2.my_bool_return():
            launcher_angle_error_button.draw()
        if error_bool_3.my_bool_return():
            spring_pull_length_error_button.draw()
        if error_bool_4.my_bool_return():
            spring_constant_error_button.draw()

        if user_input_bool.my_bool_return():
            screen.blit(velocity_surf, velocity_rect)
            screen.blit(time1_surf, time1_rect)
            screen.blit(max_h_surf, max_h_rect)
        if clear_test.check_click() and user_input_bool.my_bool_return():
            clear_bool.my_change_bool(True)

        if play_test.check_click() and user_input_bool.my_bool_return():
            if color_bool.my_bool_return():

                ball_1 = Ball(0, 0.40, velocity, float(input_boxes[1].text), 0.02, "Black")
                color_bool.my_change_bool(False)
            else:
                ball_1 = Ball(0, 0.40, velocity, float(input_boxes[1].text), 0.02, "Blue")
                color_bool.my_change_bool(True)
            ball_bool.my_change_bool(True)

        if ball_bool.my_bool_return():
            ball_1.update()

            if bright_dark_bool.my_bool_return():
                ball_1.draw(light_mode_sim)

            else:
                ball_1.draw(dark_mode_sim)

        if input_boxes[0].my_clear():
            clear_bool.my_change_bool(True)
        if input_boxes[1].my_clear():
            clear_bool.my_change_bool(True)
        if input_boxes[2].my_clear():
            clear_bool.my_change_bool(True)
            input_boxes[3].my_clear()

        if member_button.check_click():
            member_bool.my_change_bool(True)

    if member_bool.my_bool_return():
        if bright_dark_bool.my_bool_return():
            screen.blit(light_mode_member, (0,0))
        else:
            screen.blit(dark_mode_member, (0,0))
        back_to_sim_button.draw()
        home_button.draw()

        if home_button.check_click():
            start_bool.my_change_bool(True)
            member_bool.my_change_bool(False)
            sim_bool.my_change_bool(False)


        if back_to_sim_button.check_click():
            member_bool.my_change_bool(False)

    for event in pygame.event.get():
        for box in input_boxes:
            box.handle_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    pygame.display.update()
    clock.tick(60)