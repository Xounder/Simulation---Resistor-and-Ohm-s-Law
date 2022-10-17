import pygame
import sys
from settings import screen_width, screen_height, button_pos, button_neg, text_num_pos, res_mult_val, res_tol_val
from sprites import Resistor, Lamp, Batery, Button, Mult
from overlay import Overlay, InputText, Text

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Resistência')
        self.clock = pygame.time.Clock()
        
        # Sprites
        self.res = Resistor([2, 2, 1, 4])
        self.lamp = Lamp(0.02, 2)
        self.batery = Batery(2)
        # Botões
        self.res_buttons = []
        for i in range(4):
            button_plus = Button((button_pos[i]), self.res.color, i, 'sum', 4)
            button_ngtv = Button((button_neg[i]), self.res.color, i, 'sub', 4)
            self.res_buttons.append(button_plus)
            self.res_buttons.append(button_ngtv)  
        self.active = [False]
        self.clear = [False]
        self.button_play = Button((screen_width - 250, 450), self.active, 0, 'play', 1)
        self.button_pause = Button((screen_width - 120, 450), self.active, 0, 'pause', 1)
        self.button_clear= Button((screen_width - 180, 520), self.clear, 0, 'clear', 1)
        # Overlay
        self.overlay = Overlay()      
        self.text_nums = Text(25)
        # Multimetro
        self.mult = Mult()   
        self.button_mult = Button((258, 405), self.mult.frame_index, 0, 'mult', 1)   

        # corrente real
        self.cur = 0
        # resistencia da lampada
        self.r_lamp = 0
        # tensão da lampada
        self.v_lamp = 0
        # caixa de dialogos
        self.lamp_volt_diag = InputText((700, 180), (845, 185), 'V')
        self.lamp_cur_diag = InputText((460, 180), (430, 185), 'A')
        self.bat_volt_diag = InputText((screen_width/2 - 65, screen_height - 110), 
                                            (screen_width/2 + 80, screen_height - 105), 'V')
        
        # info resistor
        self.info = [False]
        self.button_info = Button((screen_width - 60, 90), self.info, 0, 'info', 2)
        self.info_surf = pygame.image.load('imgs/info.png')
        self.info_rect = self.info_surf.get_rect(center = (screen_width/2, screen_height/2))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            self.screen.fill('white')

            self.button_play.update()
            self.button_play.draw()
            self.button_pause.update()
            self.button_pause.draw()
            self.button_clear.update()
            self.button_clear.draw() 

            if not self.active[0]:
                self.lamp.reset()
                self.cur = 0
                self.r_lamp = 0
                self.v_lamp = 0
                self.lamp_volt_diag.input()
                self.lamp_cur_diag.input()
                self.bat_volt_diag.input()
            else:
                self.lamp.volt = 2 if float(self.lamp_volt_diag.txt) == 0 else float(self.lamp_volt_diag.txt)
                self.lamp.max_cur = 0.02 if float(self.lamp_cur_diag.txt) == 0 else float(self.lamp_cur_diag.txt)
                self.batery.volt[0] = 9 if float(self.bat_volt_diag.txt) == 0 else float(self.bat_volt_diag.txt) 
                # Multimetro valores
                try:
                    self.cur = round(self.batery.volt[0] / self.res.resist, 9)
                    self.r_lamp = round(self.lamp.volt / self.cur, 9) 
                    self.v_lamp = self.lamp.volt
                except Exception as e:
                    # desenha um quadrado no erro (resistor = 0)
                    pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(screen_width - 300, 205, 100, 40),  4, 3)

                self.lamp.update(self.res.resist, self.batery.volt[0], self.cur)

            self.lamp.draw()
            pygame.draw.rect(self.screen, 'black', pygame.Rect(screen_width/2 - 55, 270, 110, 250),  4, 3)
            self.batery.draw()
            self.res.update()
            self.res.draw()

            if not self.active[0]:
                for button in self.res_buttons:
                    button.update()
                    button.draw()

            if self.clear[0]:
                self.res.color[0] = 2
                self.res.color[1] = 2
                self.res.color[2] = 1
                self.res.color[3] = 4
                self.batery.volt[0] = 9
                self.lamp.reset()
                self.bat_volt_diag.txt = '0'
                self.lamp_cur_diag.txt = '0'
                self.lamp_volt_diag.txt = '0'
                self.active[0] = False
                self.clear[0] = False

                self.lamp.volt = 0
                self.lamp.max_cur = 0
                self.res.resist = 0
                self.batery.volt[0] = 0
                self.lamp.res_ideal = 0

            overlay_text = ['- Lampada:', f'      {self.lamp.volt} V', f'      {self.lamp.max_cur} A', '- Resistor:', f'      {self.res.resist} Ohms', 
                  f'      Tolerancia = {self.res.imp}%', '- Bateria:', f'      {self.batery.volt[0]} V', f'- Resistor ideal: {round(self.lamp.res_ideal, 2)}']
            self.overlay.update((screen_width - 310, 80), overlay_text)
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(screen_width - 330, 60, 300, 500),  4, 3)
            

            # Multimetro
            self.button_mult.update()
            self.mult.update(self.r_lamp, self.v_lamp, self.cur)
            self.mult.draw(self.active[0])

            # numero nas listras do resistor
            for i in range(4):
                if i < 2:
                    txt = self.res.color[i]
                else:
                    if i == 2:
                        txt = res_mult_val[self.res.color[i]]
                    else:
                        txt = res_tol_val[self.res.color[i]]
                self.text_nums.update(text_num_pos[3-i], f'{txt}', [211, 211, 255])
                self.text_nums.draw()

            self.button_info.update()
            self.button_info.draw()
            if self.info[0]:
                self.screen.blit(self.info_surf, self.info_rect)
                pygame.draw.rect(self.screen, 'black', (self.info_rect.topleft[0], self.info_rect.topleft[1], 930, 580), 3)



            pygame.display.update()        
            self.clock.tick(60)
        

game = Game()
game.run()