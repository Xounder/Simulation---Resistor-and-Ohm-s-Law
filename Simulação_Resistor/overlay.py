import pygame
from timer import Timer

class Text:
    def __init__(self):
        self.font = pygame.font.Font('C:/Users/renan/PycharmProjects/Simulação_Resistor/font/Pixeltype.ttf', 35)
        self.display_surface = pygame.display.get_surface()
    
    def draw(self):
        self.display_surface.blit(self.text, self.text_rect)

    def update(self, pos, text, color):
        self.text = self.font.render(text, False, color)
        self.text_rect = self.text.get_rect(topright = (pos))

class Overlay(Text):  
    def __init__(self):
        super().__init__()

    def draw(self):
        self.display_surface.blit(self.text, self.text_rect)

    def update(self, pos, text):
        
        for i, txt in enumerate(text):
            
            self.text = self.font.render(txt, False, (101,196,169))
            self.text_rect = self.text.get_rect(topleft = (pos[0], pos[1] + i*35))
            self.draw()
    

class InputText(Text):
    def __init__(self, pos, pos_sig, sig):
        super().__init__()
        self.txt = '0'
        self.active = False
        self.pos = pos
        self.pos_sig = pos_sig
        self.sigl = sig
        self.timer = Timer(0.15)

        self.quad_text = pygame.Surface((130, 30))
        self.quad_text.fill('white')
        self.quad_rect = self.quad_text.get_rect(topleft = (self.pos))



    def draw(self):
        self.display_surface.blit(self.quad_text, self.quad_rect)
        pygame.draw.rect(self.display_surface, 'black', pygame.Rect(self.pos[0], self.pos[1], 130, 30),  4, 3)
        self.sig = self.font.render(self.sigl, False, 'black')
        self.sig_rect = self.sig.get_rect(topleft = (self.pos_sig))
        self.display_surface.blit(self.sig, self.sig_rect)

    def update(self, pos, text, color): 
        self.text = self.font.render(text, False, color)
        self.text_rect = self.text.get_rect(topleft = (pos))
        self.display_surface.blit(self.text, self.text_rect)

    def input(self):                       
        self.draw()
        self.update((self.pos[0] + 6, self.pos[1] + 5), self.txt, 'red')
        if pygame.mouse.get_pressed()[0]:
            if self.quad_rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False
        if self.active:
            self.update((self.pos[0] + 6, self.pos[1] + 5), self.txt, 'red')
            if self.timer.run:
                self.timer.update()
            if not self.timer.run:
                self.timer.active()
                keys = pygame.key.get_pressed()
                num = ''
                if len(self.txt) < 9:
                    if keys[pygame.K_0]:
                        num = '0'
                    elif keys[pygame.K_1]:
                        num = '1'
                    elif keys[pygame.K_2]:
                        num = '2'
                    elif keys[pygame.K_3]:
                        num = '3'
                    elif keys[pygame.K_4]:
                        num = '4'
                    elif keys[pygame.K_5]:
                        num = '5'
                    elif keys[pygame.K_6]:
                        num = '6'
                    elif keys[pygame.K_7]:
                        num = '7'
                    elif keys[pygame.K_8]:
                        num = '8'   
                    elif keys[pygame.K_9]:
                        num = '9' 
                    elif keys[pygame.K_COMMA]:
                        num = '.'

                if keys[pygame.K_BACKSPACE]:
                    self.txt = self.txt[:len(self.txt)-1]
                elif keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                    self.active = False
                
                if self.txt == '0' and num != '':
                    self.txt = num
                elif num != '':
                    self.txt = self.txt + num


                        
