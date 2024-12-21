import pygame
from pygame import *
import sys
import random
pygame.init()
import os
import time
#背景音乐
pygame.mixer.music.load('bgmusic/dayLevel.opus')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)
#音效的地方，修改为一整个类
plant_sound = pygame.mixer.Sound("music/plant.ogg")
cant_plant_sound = pygame.mixer.Sound("music/buttonclick.ogg")
shoot_sound = pygame.mixer.Sound("music/shoot.ogg")
shoot_sound.set_volume(0.5)
hugeWaveApproching_sound = pygame.mixer.Sound('music/hugeWaveApproching.ogg')
zombieAttack_sound = pygame.mixer.Sound('music/zombieAttack.ogg')
zombieatkLen = zombieAttack_sound.get_length()
collectSun_sound = pygame.mixer.Sound('music/collectSun.ogg')
bulletExplode_sound = pygame.mixer.Sound('music/bulletExplode.ogg')
plantDie_sound = pygame.mixer.Sound('music/plantDie.ogg')


print(zombieatkLen)

lastplayzbatk = 0.0
bgcolor = (255,255,255)
font_color,font_size = (144, 238, 144),36  # Light Green
size = (800,560)
patch_size = 80

#地图patch类,地图类
class Patch():
    def __init__(self,x:int,y:int):
        super().__init__()
        if  (x+y)%2==0:
            self.img = pygame.image.load('imgs/map1.png')
        else :
            self.img = pygame.image.load('imgs/map2.png')
        self.rect = self.img.get_rect().move(x*patch_size,y*patch_size)

class Map():
    def __init__(self,row:int,col:int):
        self.size = row,col
        self.map_points = [[Patch(x,y) for x in range(col) ] for y in range(1,row)]
        self.has_plant = [[False for x in range(col)] for y in range(0,row)]
        # print(self.has_plant)
    

#植物相关的类
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = None
        self.rect = None
        self.live = True #是否存活
        self.price = None #价格为50
        self.hp = None
        self.frames = None
        self.cur_frame = 0
        self.pic_timeout = 3
        self.direction = 1
    def get_imgrect(self):
        return self.img,self.rect

    def load_transform(self,path):
        """返回80*80的图像"""
        img = pygame.image.load(path)
        img = pygame.transform.scale(img,(80,80))
        return img

    def get_picture_num(self,path):
        return len(os.listdir(path))
    
    def update(self):
    #更换图片，产生动态的效果
        self.pic_clock += 1
        if self.pic_clock == self.pic_timeout:    
            self.cur_frame = (self.cur_frame+1)%self.frames
            path = os.path.join(self.img_path+'/'+self.pic_names[0].split('_')[0]+'_'+\
                                           str(self.cur_frame)+'.png')
            self.img = self.load_transform(path)
            self.pic_clock = 0
            
class Sunflower(Plant):
    price = 50
    def __init__(self,col,row,gmstates):
        super().__init__()
        self.gmstates = gmstates
        self.img = pygame.image.load('imgs/sunflower.png')
        self.rect = self.img.get_rect().move(col*patch_size,row*patch_size)
        self.hp = 100
        self.live = True
        self.time = 0
        self.timeout = 200 #游戏为30帧，两秒生产一次阳光
        self.img_path = 'imgs/SunFlower'
        self.frames = self.get_picture_num(self.img_path)
        self.cur_frame = 0
        self.pic_names = os.listdir(self.img_path)
        self.pic_clock = 0
        
    def make_sun(self):
        self.time = self.time + 1
        if self.time==self.timeout:
            self.gmstates.suns.append(Sun(self.rect[0]//patch_size,self.rect[1]//80,self.gmstates))
            # self.gmstates.money += 50
            self.time = 0
        self.update()
        
class Sun(Plant):
    def __init__(self,col,row,gmstates):
        super().__init__()
        self.gmstates = gmstates
        self.img = self.load_transform('imgs\Sun\Sun_0.png')
        self.rect = self.img.get_rect().move(col*patch_size,row*patch_size)
        self.live = True
        self.time = 0
        self.timeout = 15 #游戏为30帧，一秒从植物上，移动到最顶端，消失
        self.img_path = 'imgs/Sun'
        self.frames = self.get_picture_num(self.img_path)
        self.cur_frame = 0
        self.pic_names = os.listdir(self.img_path)
        self.pic_clock = 0
        self.collect_timeout = 120 # 无人收取的最大时间
        self.collect_time = 0
        
    def click_sun(self):
        """将sun从活sun中删除，同时在死亡sun中添加一个"""
        #将money加上，在活sun列表中删除。加入diedsun中播放死亡动画
        self.live = False
        self.gmstates.suns.remove(self)
        self.gmstates.died_suns.append(self)
        self.gmstates.money += 50
        self.up_dis = (self.rect[1]-80)//self.timeout*(-1)
        collectSun_sound.play()
        return True
    
    def display_died(self):
        # print(self.up_dis)
        # print(self.rect[1])
        self.rect = self.rect.move(0,self.up_dis)
        if self.rect[1] <= 80 :
            # print(11111)
            self.gmstates.died_suns.remove(self)
    
    def update(self):
    #更换图片，产生动态的效果
        if self.live:
            self.collect_time += 1
            if self.collect_time==self.collect_timeout:
                self.collect_time = 0
                self.click_sun()
        self.pic_clock += 1
        if self.pic_clock == self.pic_timeout:    
            self.cur_frame = (self.cur_frame+1)%self.frames
            path = os.path.join(self.img_path,self.pic_names[self.cur_frame])
            self.img = self.load_transform(path)
            self.pic_clock = 0

    def load_transform(self,path):
        """sun的大小为40*40像素"""
        img = pygame.image.load(path)
        img = pygame.transform.scale(img,(60,60))
        return img
    
class PeaShooter(Plant):
    price = 100
    def __init__(self,col:int,row:int,gmstates):
        super().__init__()
        self.gmstates = gmstates
        self.img = pygame.image.load('imgs/peashooter.png')
        self.rect = self.img.get_rect().move(col*patch_size,row*patch_size)
        self.hp = 300
        self.live = True
        self.time = 0
        self.timeout = 30 #一秒射击一次
        self.fire = False
        self.img_path = 'imgs/Peashooter'
        self.frames = self.get_picture_num(self.img_path)
        self.cur_frame = 0
        self.pic_names = os.listdir(self.img_path)
        self.pic_clock = 0
        self.pic_timeout = 5
        
    def shot(self):#射击功能
        #第一次发现僵尸，立马射击一次
        state = self.fire
        self.fire = False
        for zombie in self.gmstates.zombies:
            if zombie.rect[1] == self.rect[1] and zombie.rect[0]<=size[0] and zombie.rect[0]>=self.rect[0]:#在同一行
                self.fire = True 
                break
        if self.fire:
            if not state:
                x,y = self.rect[0]/patch_size,self.rect[1]/patch_size
                self.gmstates.bullets.append(Pea(x,y))
                self.time = 0
                shoot_sound.play()
            else :
                self.time += 1
                if self.time == self.timeout:
                    self.time =0
                    x,y = self.rect[0]/patch_size,self.rect[1]/patch_size
                    self.gmstates.bullets.append(Pea(x,y))
                    shoot_sound.play()
                    
        self.update()
        
class Pea(Plant):
    """子弹类"""
    def __init__(self,x,y,speed=5):
        super().__init__()
        self.img = pygame.image.load('imgs/PeaNormal_0.png')
        self.rect = self.img.get_rect().move(x*patch_size+70,y*patch_size+15)
        self.live = True
        self.speed = speed
        self.atp = 15
    def move(self):
        self.rect = self.rect.move(self.speed,0) #在X方向上移动
        pass #这里要添加与僵尸碰撞检测的代码
        if self.rect.right > size[0] : #飞出屏幕，子弹消失
            self.live = False
    
    def hit(self,zombie):#攻击一个僵尸，然后子弹消失
        zombie.hp -= self.atp
        self.live = False
        bulletExplode_sound.play()

class Zombie(Plant):
    speed = -1
    def __init__(self,x,y,gmstates):
        super().__init__()
        self.gmstates = gmstates
        self.img = self.load_transform('imgs/jiaxue.jpg')
        self.rect = self.img.get_rect().move(x*patch_size,y*patch_size)
        self.hp = 100
        self.atp = 1
        self.live = True
        self.ismove = True
        self.img_path = 'imgs\FootballZombie'
        self.eat_img_path = 'imgs\FootballZombieAttack'
        self.died_img_path = 'imgs\FootballZombieDie'
        self.frames = self.get_picture_num(self.img_path)
        self.eat_prames = self.get_picture_num(self.eat_img_path)
        self.died_frames = self.get_picture_num(self.died_img_path)
        self.cur_frame = 0
        self.eat_curframe = 0
        self.died_curframe = 0
        self.pic_names = os.listdir(self.img_path)
        self.eat_pic_names = os.listdir(self.eat_img_path)
        self.died_pic_names = os.listdir(self.died_img_path)
        self.pic_clock = 0
        self.pic_timeout = 3
        self.eat_timeout = 1
        self.died_clock = 0
        
        self.died_timeout = len(self.died_pic_names)
        
    def move(self):
        if self.ismove:
            self.rect = self.rect.move(self.speed,0)
        if self.rect.left < 0 :
            self.gmstates.GAMEOVER = True
        self.update()
        
    def eat_plant(self,plant):
        global lastplayzbatk
        plant.hp -= self.atp
        cur_time = time.time()
        # print(cur_time-lastplayzbatk)
        if (cur_time-lastplayzbatk) >= zombieatkLen:
            lastplayzbatk = cur_time
            zombieAttack_sound.play()

    def update(self):
    #更换图片，产生动态的效果
        if self.ismove : 
            self.pic_clock += 1
            if self.pic_clock == self.pic_timeout:    
                self.cur_frame = (self.cur_frame+1)%self.frames
                path = os.path.join(self.img_path,self.pic_names[self.cur_frame])
                self.img = self.load_transform(self.img_path+'/'+self.pic_names[0].split('_')[0]+'_'+\
                                           str(self.cur_frame)+'.png')
                self.pic_clock = 0
        else :
            self.pic_clock += 1
            self.img = self.load_transform(self.eat_img_path+'/'+self.eat_pic_names[0].split('_')[0]+'_'+\
                                           str(self.eat_curframe)+'.png') 
            if self.pic_clock >= self.eat_timeout: 
                # print(self.eat_curframe)  
                self.eat_curframe = (self.eat_curframe+1)%self.eat_prames
                path = os.path.join(self.eat_img_path,self.eat_pic_names[self.eat_curframe])
                # print(self.eat_img_path+'/'+self.eat_pic_names[0].split('_')[0]+'_'+\
                                        #    str(self.eat_curframe)+'.png')
                self.img = self.load_transform(self.eat_img_path+'/'+self.eat_pic_names[0].split('_')[0]+'_'+\
                                           str(self.eat_curframe)+'.png')
                self.pic_clock = 0

    def set_died(self):
        self.img = self.load_transform(self.died_img_path+'/'+self.died_pic_names[0])
        
    def display_died(self):
        self.died_clock += 1
        if(self.died_clock==3):
            self.died_curframe += 1
            if self.is_died_pic_over():
                self.gmstates.died_zombies.remove(self)
                return None 
            self.img = self.load_transform(self.died_img_path+'/'+self.died_pic_names[self.died_curframe].split('_')[0]+'_'+\
                                           str(self.died_curframe)+'.png')
            self.died_clock = 0
        self.gmstates.screen.blit(*(self.get_imgrect()))    
        
    def is_died_pic_over(self):
        if self.died_curframe == self.died_frames:
            return True
        return False
    
class Viewer():
    def __init__(self,screen,gmstates) -> None:
        self.gmstates = gmstates
        self.screen = screen
        self.shovel_img = self.load_transform('imgs\shovel.png')
        
    def display_map(self):
        self.screen.fill(bgcolor)
        for row in self.gmstates.map.map_points:
            for patch in row:
                self.gmstates.screen.blit(patch.img,patch.rect)
                
    def display(self,plants,bullets,zombies):
        for plant in plants.copy():
            if not plant.live:
                plants.remove(plant)
                continue
            if isinstance(plant,Sunflower):
                plant.make_sun()
            elif isinstance(plant,PeaShooter):
                plant.shot()
            self.gmstates.screen.blit(*(plant.get_imgrect()))

        for zombie in zombies.copy():
            if not zombie.live:
                zombies.remove(zombie)
                zombie.set_died()
                self.gmstates.died_zombies.append(zombie)
                continue
            zombie.move()
            self.gmstates.screen.blit(*(zombie.get_imgrect()))

        for died_zombie in self.gmstates.died_zombies.copy():
            died_zombie.display_died()
            # print(died_zombie.died_curframe)
            # self.gmstates.screen.blit(*(died_zombie.get_imgrect()))
        
        # if len(self.gmstates.died_zombies)>0 :
        #     print(len(self.gmstates.died_zombies))
        for bullet in bullets.copy():
            if not bullet.live :
                bullets.remove(bullet)   
                continue         
            self.gmstates.screen.blit(*(bullet.get_imgrect()))
            bullet.move()

        for sun in self.gmstates.suns.copy():
            sun.update()
            self.gmstates.screen.blit(*(sun.get_imgrect()))
            
        # print(len(self.gmstates.died_suns))
        for died_sun in self.gmstates.died_suns.copy():
            died_sun.update()
            died_sun.display_died()
            self.gmstates.screen.blit(*(died_sun.get_imgrect()))
            # self.gmstates.screen.blit(died_sun.img,died_sun.rect)
        
    def display_screbd(self):
        font = pygame.font.SysFont('Arial',40)
        score_text = font.render(f"score:{self.gmstates.score}",True,font_color)
        money_text = font.render(f"sun:{self.gmstates.money}",True,font_color)
        zombies_text = font.render(f"remain zombies:{self.gmstates.remain_zombies}",True,font_color)
        level_text = font.render(f"Level:{self.gmstates.level}",True,font_color)
        self.screen.blit(money_text,(10,20))
        self.screen.blit(score_text,(10+2*patch_size,20))
        self.screen.blit(zombies_text,(10+4*patch_size,20))
        self.screen.blit(level_text,(10+8*patch_size,20))
        
        
    def display_gameover(self):
        font = pygame.font.SysFont('Arial',60)
        message_text = font.render("Zombie eat your brain!!!!!!",False,(255,0,0))
        # print(message_text.get_rect())
        self.screen.blit(message_text,(size[0]//2-message_text.get_rect().width//2,
                        size[1]//2-message_text.get_rect()[1]//2))
        pygame.display.flip()
        
    def display_win(self):
        font = pygame.font.SysFont('Arial',60)
        message_text = font.render("A horde of zombies is coming!!!",False,(250,87,47))
        # print(message_text.get_rect())
        self.screen.blit(message_text,(size[0]//2-message_text.get_rect().width//2,
                        size[1]//2-message_text.get_rect()[1]//2))
        pygame.display.flip()
    
    def display_shovel(self,mos_pos):
        shovel_rect = self.shovel_img.get_rect()
        shovel_rect.center = mos_pos
        # print(shovel_rect)
        self.gmstates.screen.blit(self.shovel_img,shovel_rect)
    
    def load_transform(self,path):
        """返回80*80的图像"""
        img = pygame.image.load(path)
        img = pygame.transform.scale(img,(40,40))
        return img

        
class Generator():
    timeout = 30
    def __init__(self,gmstates):
        self.gmstates = gmstates
        self.money_timeout = 90
        self.money_time = 0
        self.time = 0
        
    def init_zombies(self):
        for i in range(1,7):
            dis = random.randint(1,6)
            zombie = Zombie(self.gmstates.map.size[1]+dis,i,self.gmstates)
            self.gmstates.zombies.append(zombie)
            print(f"僵尸个数:{len(self.gmstates.zombies)}")

    def get_zombie(self):
        if self.gmstates.remain_zombies > 0: # 如果还有僵尸剩余，产生一个僵尸
            row = random.randint(1,6)
            dis  = random.randint(1,6)
            zombie = Zombie(self.gmstates.map.size[1]+dis,row,self.gmstates)
            self.gmstates.zombies.append(zombie)
            self.gmstates.remain_zombies -= 1
        print(f"僵尸个数:{len(self.gmstates.zombies)},钱数:{self.gmstates.money},剩余僵尸数：{self.gmstates.remain_zombies}")

    def genmoney(self):
        self.money_time += 1
        if self.money_time == self.money_timeout:
            self.gmstates.money += 40
            self.money_time = 0
            
    def step(self):#运行一个时间步
        self.time += 1
        if self.time==self.timeout:
            self.get_zombie()
            self.timeout = random.randint(30,60)
            self.time = 0
        self.genmoney()

class GameState():
    def __init__(self):
        """数据接口"""
        self.GAMEOVER = False
        self.money = 200
        self.score = 0
        self.remain_zombies = 40
        self.plants = []
        self.bullets = []
        self.zombies = []
        self.died_zombies = []
        self.suns = []
        self.died_suns = []
        self.screen = pygame.display.set_mode(size)
        self.map = Map(7,10)
        self.level = 1
        self.base_zombie_num = 40
        
class Controller():
    def __init__(self,gmstates):
        #存储游戏的状态
        self.gmstates = gmstates            
        self.viewer = Viewer(self.gmstates.screen,self.gmstates)
        self.generator = Generator(self.gmstates)
        self.clock = pygame.time.Clock()
        self.is_shovel_mode = False
        
    def handle_events(self):
        for event in pygame.event.get():
                if event.type in (QUIT,):
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self.is_shovel_mode = True
                    pygame.mouse.set_visible(False)
                    # #画面中显示铲子
                    # self.viewer.display_shovel(pygame.mouse.get_pos())
                    
                elif event.type == KEYUP and event.key == K_SPACE:
                    self.is_shovel_mode = False
                    pygame.mouse.set_visible(True)                   
                #铲子铲掉植物
                elif event.type == MOUSEBUTTONDOWN and self.is_shovel_mode:
                    mos_pos = pygame.mouse.get_pos()
                    x,y = mos_pos[0]//patch_size,mos_pos[1]//patch_size
                    #遍历植物
                    for plant in self.gmstates.plants:
                        if plant.rect.collidepoint(mos_pos):
                            self.gmstates.plants.remove(plant)
                            #将田块设置为空白
                            self.gmstates.map.has_plant[y][x] = False
                            plant_sound.play()
                    
                elif event.type == MOUSEBUTTONDOWN and not self.is_shovel_mode:
                    pos = event.pos
                    x,y = pos[0]//patch_size,pos[1]//80 #获取点击的田块的坐标
                    if y < 1 or y > 6 or x < 0 or x > 9 :#非法的种植位置，不进行任何操作
                        continue
                    if event.button == 1:#左键种植太阳花
                        is_click_sun = False
                        #处理点击阳光的逻辑
                        mous_pos = pygame.mouse.get_pos()
                        for sun in self.gmstates.suns.copy():
                            if sun.rect.collidepoint(mous_pos):
                                sun.click_sun()
                                is_click_sun = True
                                
                        if not self.gmstates.map.has_plant[y][x] and self.gmstates.money >= Sunflower.price:
                            plant_sound.play()
                            sunflower = Sunflower(x,y,self.gmstates)
                            self.gmstates.plants.append(sunflower)
                            self.gmstates.money -= Sunflower.price
                            self.gmstates.map.has_plant[y][x] = True
                        else :
                            if not is_click_sun:
                                cant_plant_sound.play()
                        
                    elif event.button == 3:#右键种植豌豆射手
                        if not self.gmstates.map.has_plant[y][x] and self.gmstates.money >= PeaShooter.price:
                            plant_sound.play()
                            peashooter = PeaShooter(x,y,self.gmstates)
                            self.gmstates.plants.append(peashooter)
                            self.gmstates.money -= PeaShooter.price
                            self.gmstates.map.has_plant[y][x] = True
                        else :
                            cant_plant_sound.play()
                    
                            
    def collision_dect(self):
        #检测子弹和僵尸的碰撞
        for bullet in self.gmstates.bullets.copy():
            for zombie in self.gmstates.zombies.copy():
                if bullet.rect.colliderect(zombie.rect):
                    bullet.hit(zombie)
                    if zombie.hp < 0:#杀死一个僵尸
                        zombie.live = False
                        self.gmstates.score += 10
                    bullet.live = False
        #检测僵尸和植物的碰撞
        for zombie in self.gmstates.zombies:
            is_move = True
            for plant in self.gmstates.plants.copy():
                if zombie.rect.colliderect(plant.rect):
                    zombie.eat_plant(plant)
                    if(plant.hp<0):
                        plantDie_sound.play()
                        self.gmstates.plants.remove(plant)
                        x,y = plant.rect[0]//patch_size,plant.rect[1]//patch_size
                        # print(x,y)
                        self.gmstates.map.has_plant[y][x] = False
                    is_move = False
            zombie.ismove = is_move
            
    
    def gen_element(self):
        self.generator.step()
        
    def check_win(self):
        if self.gmstates.remain_zombies==0 and len(self.gmstates.zombies)==0:
            self.viewer.display_win()
            pygame.display.flip()
            hugeWaveApproching_sound.play()
            pygame.time.delay(1500) # 等待1.5秒后，进行下一波
            self.gmstates.level += 1
            #僵尸移动速度变快
            Zombie.speed *= (1+self.gmstates.level/10)
            self.gmstates.base_zombie_num += 10
            self.gmstates.remain_zombies = self.gmstates.base_zombie_num
            #出僵尸的速度变快
            if self.generator.timeout > 10:
                self.generator.timeout -= 2
                        
    def run(self):
        self.generator.init_zombies()
        while not self.gmstates.GAMEOVER:
            #1获取事件，绘制基本元素
            self.handle_events()        
            self.viewer.display_map()
            self.viewer.display(self.gmstates.plants,self.gmstates.bullets,self.gmstates.zombies)
            self.viewer.display_screbd()
            
            #2碰撞检测
            self.collision_dect()
            
            #3僵尸的生成，阳光生成，
            self.gen_element()
            
            #4检查是否需要绘制铲子
            if self.is_shovel_mode:
                self.viewer.display_shovel(pygame.mouse.get_pos())
            #4检查游戏是否胜利
            self.check_win()       
            #渲染屏幕
            pygame.display.flip()
            self.clock.tick(30)
        
gmstates = GameState()
controller = Controller(gmstates)
controller.run()    

if gmstates.GAMEOVER:
    print(f"test---zombienums{len(gmstates.zombies)}")
    for zombie in gmstates.zombies:
        print(zombie.rect[:2])
    controller.viewer.display_gameover()
    while 1 :
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
    