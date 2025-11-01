# Импортировал библиотеки pygame и random
import pygame as pg
import random

# Начало работы, выставил размер экрана, назвал окно, выставил шрифт и размер символов
pg.init()
screen = pg.display.set_mode((600, 800))
pg.display.set_caption('Убийца блоков')
font = pg.font.SysFont(None, 24)

# Вставил в переменные RGB-цвета
BLACK = (0, 0, 0)
RED = (125, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
GRAY = (148, 148, 148)

# Вызвал картинку и звук в свои переменные
# переменные самолёта
airplane_img = pg.image.load('src\\images\\airplane.png').convert_alpha() # вызываем картинку в переменную для дальнейшего использования
airplane_sound = pg.mixer.Sound('src\\sounds\\death_airplane.mp3')

# переменные блока
block_img = pg.image.load('src\\images\\blocks.png').convert_alpha() # вызываем картинку в переменную для дальнейшего использования
block_sound = pg.mixer.Sound('src\\sounds\\death_block.mp3')

# переменные выстрела
hit_img = pg.image.load('src\\images\\hit.png').convert_alpha() # вызываем картинку в переменную для дальнейшего использования
hit_sound = pg.mixer.Sound('src\\sounds\\hit.mp3')
hit_sound.set_volume(0.05) # выставил громкость выстрела 5/100

score = 0 # Счёт убитых блоков

# Вставил фото как объект, настроил скорость, здоровье 100хп, удобный вызов фотографии самолёта
airplane = { 
    "img": airplane_img,
    'speed': [0, 0],
    'health': 100,
    'rect': airplane_img.get_rect()
}

# Получил хитбокс самолёта и параметры x, y
airplane['rect'] = airplane['img'].get_rect()
airplane['rect'].x = 300
airplane['rect'].y = 700

# Создал списки для блока и выстрела
blocks = []
hits = []

# Константы: задержка выстрела, задержка блока каждого слоя
SHOT_DELAY = 0.3 * 1000
BLOCK_LAYER_DELAY = 5 * 1000
# Переменные: время поледнего выстрела и последнего выпущенного слоя
last_shot_time = 0
last_block_layer_time = 0

# Cоздание переменной время
clock = pg.time.Clock()

# Переменная для бесконечного цикла
running = True
# Бесконечный цикл
while running:
    current_time = pg.time.get_ticks()
    for event in pg.event.get(): 
        if event.type == pg.QUIT:
            running = False
        #обработка движения самолёта:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                airplane['speed'][1] -= 2
            elif event.key == pg.K_s:
                airplane['speed'][1] += 2
            elif event.key == pg.K_a:
                airplane['speed'][0] -= 2
            elif event.key == pg.K_d:
                airplane['speed'][0] += 2
        if event.type == pg.KEYUP:
            if event.key == pg.K_w or event.key == pg.K_s: airplane['speed'][1] = 0
            if event.key == pg.K_a or event.key == pg.K_d: airplane['speed'][0] = 0

    if current_time - last_shot_time > SHOT_DELAY:
        hits.append({
            'img': hit_img,
            "speed": [0, -30],
            'rect': pg.Rect(airplane['rect'].x+45, airplane['rect'].y, 10, 30)
        })
        hit_sound.play() # воспроизведение звука выстрела
        last_shot_time = current_time

    if current_time - last_block_layer_time > BLOCK_LAYER_DELAY:
        for j in range(10):
            blocks.append({
                'img': block_img,
                "speed": [0, 1],
                'rect': pg.Rect((j * 59) + 10, -50, 49, 49),
                'health': 30
            })
        last_block_layer_time = current_time

    #!что на поле
    screen.fill(WHITE) #цвет фона серый
    txt1 = font.render(f"Ваш счёт: {score}", True, BLACK) 
    screen.blit(txt1, (490, 0))
    airplane['rect'] = airplane['rect'].move(airplane['speed'])

    pg.draw.rect(screen, GRAY, airplane['rect'], 1)
    screen.blit(airplane['img'], airplane['rect'])

    if airplane['rect'].left < 0: airplane['rect'].left = 0
    if airplane['rect'].right > 600: airplane['rect'].right = 600
    if airplane['rect'].top < 0: airplane['rect'].top = 0
    if airplane['rect'].bottom > 800: airplane['rect'].bottom = 800

    for hit in hits:
        hit['rect'] = hit['rect'].move(hit['speed'])
        pg.draw.rect(screen, GRAY, hit['rect'], 1)
        screen.blit(hit['img'], hit['rect'])

    if airplane['health'] <= 0:
        airplane_sound.play() # звук смерти самолётика
        print('You dead, Игра закончена!')
        pg.time.wait(500)
        running = False

    for block in blocks:
        block['rect'] = block['rect'].move(block['speed'])
        pg.draw.rect(screen, GRAY, block['rect'], 1)
        screen.blit(block['img'], block['rect'])
        
        if block['health'] <= 0: # если у блока меньше или равно 0 хп то ...
            blocks.remove(block) # то он изчезает, и..
            block_sound.play() # звук удаления блока
            score += 1 # и счёт (переменная) выростает на 1балл, фууух

        for hit in hits:
            if hit['rect'].colliderect(block['rect']):
                block['health'] -= 10
                hits.remove(hit)
                              
        #
        if block['rect'].colliderect(airplane['rect']):
            airplane['health'] -= 10 # самолёт теряет 10хп
            blocks.remove(block) # удаление блока
            
        
    pg.display.update() #обновление дисплея каждый раз
    clock.tick(60) # 60 FPS

pg.quit()
