# напиши свій код тут
key_switch_camera = "c"  # камера прив'язана до героя чи ні
key_switch_mode = "z"  # можна проходити крізь перешкоди чи ні


key_forward = "w"  # крок вперед (куди дивиться камера)
key_back = "s"  # крок назад
key_left = "a"  # крок вліво (вбік від камери)
key_right = "d"  # крок вправо
key_up = "e"  # крок вгору
key_down = "q"  # крок вниз


key_turn_left = "n"  # поворот камери праворуч (а світу - ліворуч)
key_turn_right = "m"  # поворот камери ліворуч (а світу – праворуч)


key_build = "b"  # побудувати блок перед собою
key_destroy = "v"  # зруйнувати блок перед собою





class Hero:
    def __init__(self, pos, land):
        self.land = land
        self.mode = True  # режим проходження крізь усе
        self.hero = loader.loadModel("smiley")
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
    
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.setR(0)
        base.camera.setP(0)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn == True:
            self.cameraUp()
        else:
            self.cameraBind()

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
          self.try_move(angle)
    
    def try_move(self, angle):
        """переміщається, якщо може"""
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            # маємо вільно. Можливо, треба впасти вниз:
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            # маємо зайнято. Якщо вийде, заберемося на цей блок:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
                # не вийде забратися - стоїмо на місці

    def just_move(self, angle):
       '''переміщається у потрібні координати у будь-якому випадку'''
       pos = self.look_at(angle)
       self.hero.setPos(pos)

    def look_at(self, angle):
       ''' повертає координати, в які переміститься персонаж, що стоїть у точці (x, y),
        якщо він робить крок у напрямку angle'''


       x_from = round(self.hero.getX())
       y_from = round(self.hero.getY())
       z_from = round(self.hero.getZ())


       dx, dy = self.check_dir(angle)
       x_to = x_from + dx
       y_to = y_from + dy
       return x_to, y_to, z_from

    

    def accept_events(self):
        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + "-repeat", self.turn_left)

        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + "-repeat", self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)

        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)



    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def back(self):
       angle = (self.hero.getH()+180) % 360
       self.move_to(angle)

    def forward(self):
       angle =(self.hero.getH()) % 360
       self.move_to(angle)
       
    def left(self):
       angle = (self.hero.getH() + 90) % 360
       self.move_to(angle)


    def right(self):
       angle = (self.hero.getH() + 270) % 360
       self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    

    def check_dir(self, angle):
        """повертає заокруглені зміни координат X, Y,
        відповідні переміщенню у бік кута angle.
        Координата Y зменшується, якщо персонаж дивиться на кут 0,
        та збільшується, якщо дивиться на кут 180.
        Координата X збільшується, якщо персонаж дивиться на кут 90,
        та зменшується, якщо дивиться на кут 270.
        кут 0 (від 0 до 20)      ->        Y - 1
        кут 45 (від 25 до 65)    -> X + 1, Y - 1
        кут 90 (від 70 до 110)   -> X + 1
        від 115 до 155            -> X + 1, Y + 1
        від 160 до 200            ->        Y + 1
        від 205 до 245            -> X - 1, Y + 1
        від 250 до 290            -> X - 1
        від 290 до 335            -> X - 1, Y - 1
        від 340                   ->        Y - 1"""
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)
