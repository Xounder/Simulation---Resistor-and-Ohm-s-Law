from cgitb import text
import pygame
from settings import *
from timer import Timer
from overlay import Text

class Stripe:
    def __init__(self, pos, tam_x, tam_y, color):
        self.image = pygame.Surface((tam_x, tam_y))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (pos))
    
    def atualize_color(self, color_num, num):
        if num >= 2:
            if num == 2:
                color = res_mult_color[color_num]
            else:
                color = res_tol_color[color_num]
        else:
            color = res_color[color_num] 
        self.image.fill(color)

class Resistor:
    def __init__(self, color):
        self.display_surface = pygame.display.get_surface()
        # valores do resistor
        self.resist = round((color[0]*10 + color[1]) * 10**res_mult_val[color[2]], 2)
        self.imp =  res_tol_val[color[3]]
        self.color = color
        # resistor
        self.tam = (40,90)
        self.image = pygame.Surface(self.tam)
        self.image.fill('violet')
        self.rect = self.image.get_rect(center = (screen_width/2 -53, screen_height/2 + 30))
        #tamanho e posição do fio
        tam_y = self.tam[0] + self.tam[1] - 20
        tam_x = 4
        pos_x = self.rect.x - (tam_x - self.tam[0])/2
        pos_y = self.rect.y + (self.tam[1]/2 - tam_y/2)
        # fio do resistor
        self.line = pygame.Surface((tam_x, tam_y))
        self.line.fill('grey')
        self.line_rect = self.line.get_rect(topleft = (pos_x, pos_y))
        # listras resitor
        self.stripes = []
        for i in range(3, -1, -1):
            t_tam_x = 14
            pos_y = self.rect.y + self.tam[1]/(self.tam[0]/10) + i*(t_tam_x + 3) + 3
            pos_x = self.rect.x + self.tam[0]/2
            t = Stripe((pos_x, pos_y), self.tam[0], t_tam_x, res_color[self.color[i]])
            self.stripes.append(t)
            self.display_surface.blit(t.image, t.rect)

    def draw(self):
        self.display_surface.blit(self.line, self.line_rect)
        self.display_surface.blit(self.image, self.rect)
        for stripe in self.stripes:
            self.display_surface.blit(stripe.image, stripe.rect)

    def update(self):
        self.resist = round((self.color[0]*10 + self.color[1]) * 10**res_mult_val[self.color[2]], 2)
        self.imp = res_tol_val[self.color[3]]
        for i, stripe in enumerate(self.stripes):
            stripe.atualize_color(self.color[i], i)
           

class Lamp:
    def __init__(self, cur, volt):
        self.display_surface = pygame.display.get_surface()
        # lampada frames
        self.import_assets()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (screen_width/2, screen_height/5))
        # lamapada valores
        self.max_cur = cur
        self.volt = volt
        self.res_ideal = 0
    
    def import_assets(self):
        lamp_surf = [pygame.image.load(f'imgs/lamp/{i}.gif').convert_alpha() for i in range(1, 10)]
        lamp_x = lamp_surf[0].get_width()/2
        lamp_y = lamp_surf[0].get_height()/2
        self.frames = [pygame.transform.scale(lamp_surf[i], (lamp_x,lamp_y)) for i in range(len(lamp_surf))]
    
    def reset(self):
        #self.res_ideal = 0
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def draw(self):
        self.display_surface.blit(self.image, self.rect)
    
    def animate(self, res_resist, volt, cur_mult):
        #ajustar
        #self.res_ideal = (volt - self.volt)/ self.max_cur (antigo)
        self.res_ideal = volt / self.max_cur

        if self.max_cur/4 <= cur_mult <= self.max_cur/3:
            self.frame_index = 1
        elif self.max_cur/1.35 <= cur_mult <= self.max_cur:
            self.frame_index += 0.5
            if self.frame_index >= len(self.frames)-1:
                self.frame_index = len(self.frames)-1
        elif self.max_cur/4 <= cur_mult < self.max_cur/1.35:
                self.frame_index += 0.3
                if self.frame_index >= 6:
                    self.frame_index = 6
        else:
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, res_resist, volt, cur_mult):
        self.animate(res_resist, volt, cur_mult)


class Batery:
    def __init__(self, cur, volt=9):
        self.cur = cur
        self.volt = [volt]
        self.image = pygame.image.load('imgs/bateria/1.jpg').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width/2, 540))
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.display_surface.blit(self.image, self.rect)


class Button:
    def __init__(self, pos, r_color, r_num, name, div,):
        self.display_surface = pygame.display.get_surface()
        self.r_color = r_color
        self.res_number = r_num
        self.name = name
        self.timer = Timer(0.3)
        # active
        self.active = r_color
        self.clear = r_color
        # imagem
        if self.name == 'mult':
            self.image = pygame.Surface((110,110))
        else:
            button = pygame.image.load(f'imgs/button/{name}.png').convert_alpha()
            self.image = pygame.transform.scale(button, (button.get_width()/div, button.get_height()/div))
        self.rect = self.image.get_rect(center = (pos))

    def input(self):
        if not self.timer.run:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    self.timer.active()
                    # verificando a referencia da listra
                    if self.res_number >= 2:
                        if self.res_number == 2:
                            reference = res_mult_color  
                        else:
                            reference = res_tol_color
                    else:
                        reference = res_color   
                    if self.name.split('_')[0] == 'sum':

                        self.r_color[self.res_number] += 1 
                        if self.r_color[self.res_number] >= len(reference):
                            self.r_color[self.res_number] = 0

                    elif self.name.split('_')[0] == 'sub':
                        if self.r_color[self.res_number] > 0:
                            self.r_color[self.res_number] -= 1
                        else:
                            self.r_color[self.res_number] = len(reference)-1
                    
                    elif self.name == 'play':
                        self.active[0] = True 
                    elif self.name == 'pause':
                        self.active[0] = False
                    elif self.name == 'clear':
                        self.clear[0] = True
                    elif self.name == 'info':
                        self.active[0] = not self.active[0]
                    elif self.name == 'mult':
                        self.r_color[self.res_number] += 1 
                        if self.r_color[self.res_number] >= 3:
                            self.r_color[self.res_number] = 0
                    
    
    def draw(self):
        self.display_surface.blit(self.image, self.rect)
    
    def update(self):
        self.input()
        if self.timer.run:
            self.timer.update()


class Mult:
    def __init__(self): 
        self.display_surface = pygame.display.get_surface()
        # imagens
        self.import_assets()
        self.frame_index = [0]
        self.image = self.frames[self.frame_index[0]]
        self.rect = self.image.get_rect(center = (screen_width/5, screen_height/2))
        # valores
        self.volt = 0
        self.ohm = 0
        self.amp = 0
        # texto
        self.text_surf = Text(35)
        self.txt = f'{self.volt}'

    def import_assets(self):
        self.frames = []
        for i in range(3):
            path = f'imgs/multimetro/{i}.jpg'
            self.frames.append(pygame.image.load(path).convert_alpha())
        
    def draw(self, active):
        self.display_surface.blit(self.image, self.rect)
        self.text_surf.update((320, 255), self.txt, 'black')
        self.text_surf.draw()
        if active:
            # fios do multimetro
            pygame.draw.line(self.display_surface, 'red', (342,490), (500, 490), 6)
            pygame.draw.line(self.display_surface, 'red', (500,493), (500, 330), 6)
            pygame.draw.line(self.display_surface, 'red', (498,330), (588, 330), 6)

            pygame.draw.line(self.display_surface, 'gray', (180,500), (180, 550), 6)
            pygame.draw.line(self.display_surface, 'gray', (178,550), (450, 550), 6)
            pygame.draw.line(self.display_surface, 'gray', (450,553), (450, 300), 6)
            pygame.draw.line(self.display_surface, 'gray', (448,300), (694, 300), 6)
    
    def update(self, ohm, volt, amp):
        self.ohm = ohm
        self.volt = volt
        self.amp = amp
        if self.frame_index[0] == 0:
            self.txt = f'{self.volt}'
        elif self.frame_index[0] == 1:
            self.txt = f'{self.ohm}'
        else:
            self.txt = f'{self.amp}'
        self.image = self.frames[self.frame_index[0]]
        

        