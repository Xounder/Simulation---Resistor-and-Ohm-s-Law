screen_width = 1280
screen_height = 720

# codigo de cores resistor
res_color = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'grey', 'white']
res_mult_color = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', [218, 165, 32], [176, 176, 174]]
res_tol_color = ['brown', 'red', 'orange', 'yellow', [218, 165, 32], [176, 176, 174]]
# valor do multiplicador e da tolerancia do resistor
res_mult_val = [0, 1, 2, 3, 4, 5, 6, 7, -2, -1]
res_tol_val = [1, 2, 3, 4, 10, 5]
# posição dos botões de (+,-) do resistor
x = 555
y = 422
space_y = 18
button_pos = [(x, y), (x, y - space_y), (x , y - space_y*2), (x, y - space_y*3)]
x = 618
button_neg = [(x, y), (x, y - space_y), (x, y - space_y*2), (x, y - space_y*3)]

button_bat = [(580, 620),(620, 620), (660, 620),(700, 620)]
