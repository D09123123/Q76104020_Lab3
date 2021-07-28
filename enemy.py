import pygame
import math
import os
from settings import PATH, RED, WHITE, PATH_2

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

class Enemy:
    def __init__(self):
        global wave_count
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.i = 0            #其實就是 self.path_index = 0, 當初沒看到, 所以就用 self.i
        self.counter = 0
        self.initialize = 1   #為了只初始化一次的變數，下面會解釋         
        
        self.path = PATH      #一開始還是要先給值，等等再判斷要以哪裡為出發點    
        self.x, self.y = self.path[0]
        self.ax ,self.ay = self.path[self.i]         
        self.bx ,self.by = self.path[self.i+1]
        
    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win, WHITE, [self.x - self.width // 2, self.y - self.height // 2 - 20, 60, 5]) #max health
        pygame.draw.rect(win, RED, [self.x - self.width // 2, self.y - self.height // 2 - 20, 60*(self.health/self.max_health), 5])                                                                                                                 #current health
        # ...(to be done)
        

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        stride = 1
        if self.initialize == 1:                        #判斷要在哪裡為出發點的開關
        
            if self.wave % 2 == 1:                      #如果是奇數次按n鍵的話，執行這裡,從左邊開始出兵 wave的值在 main 生成
                self.path = PATH                        #引用從左邊的路徑
                self.x, self.y = self.path[0]
                self.ax ,self.ay = self.path[self.i]         
                self.bx ,self.by = self.path[self.i+1]
                self.initialize = 0                     #讓Enemy()不會再判斷哪裡為出發點，不會讓程式再跑進這個條件式，造成一直初始化
            else:                                       #如果是偶數次按n鍵的話，執行這裡,從右邊開始出兵
                self.path = PATH_2                      #引用從右邊的路徑
                self.x, self.y = self.path[0]
                self.ax ,self.ay = self.path[self.i]         
                self.bx ,self.by = self.path[self.i+1]
                self.initialize = 0                     #讓Enemy()不會再判斷哪裡為出發點，不會讓程式再跑進這個條件式，造成一直初始化
        distance_A_B = math.sqrt((self.ax - self.bx)**2 + (self.ay - self.by)**2)
        max_count = int(distance_A_B / stride)  # total footsteps that needed from A to B

        if self.counter < max_count:
            unit_vector_x = (self.bx - self.ax) / distance_A_B
            unit_vector_y = (self.by - self.ay) / distance_A_B
            delta_x = unit_vector_x * stride
            delta_y = unit_vector_y * stride

            # update the coordinate and the counter
            self.x += delta_x
            self.y += delta_y
            self.counter += 1
        else:                                          #換點
            self.i += 1
            self.ax, self.ay = self.path[self.i]  
            self.bx, self.by= self.path[self.i+1]
            self.counter = 0 
        # ...(to be done)
    

class EnemyGroup:
    def __init__(self):
        self.campaign_count = 0
        self.campaign_max_count = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3 

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        self.campaign_count += 1                                  #每跑一次 count 一次
        if self.campaign_count == self.campaign_max_count:        #當跑了 120 次 (120 frames)
            if len(self.reserved_members) != 0:                   #判斷是否有尚未出兵的怪物 reserved_members
                self.expedition.append(self.reserved_members[0])  #如果有就放到 expedition 開始出兵
                self.reserved_members.pop(0)                      #把尚未出兵的紀錄 pop 掉
            self.campaign_count = 0                               #重新 count 一次 
                                                                  #反覆動作
        # ...(to be done)

        

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        for j in range(num):     #產生怪物,main中預設 num = 3
            self.reserved_members.append(Enemy())
        # ...(to be done)
       

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





