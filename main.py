

# Using Ursina Engine
# BLOCK LOCK : Miniature Minecraft

import random as r
from ursina import *                                    # importing the Ursina Engine
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()                                          

window.fps_counter.enabled = True
window.exit_button.visible = True

sound = Audio('sound.mp3', autoplay=False)              #defined audio , will be played on every block placement

blocks = [
    load_texture('assets/grass.png'), # 0
    load_texture('assets/grass.png'), # 1
    load_texture('assets/bush.png'),  # 2
    load_texture('assets/stone.png'), # 3
    load_texture('assets/gold.png'),  # 4
    load_texture('assets/lava.png'),  # 5
   
]

t = 1                                            #stores the texture code 
#stores position of blocks and its texture
pos = list()
tex = list()

def input(key):
    global t, hand
    if key.isdigit(): # if we press 4 , t = 4 , texture block[t] = gold
        t = int(key)
        if t >= len(blocks):
            t = len(blocks) - 1
        hand.texture = blocks[t]

sky = Entity(                                   # defining sky
    parent=scene,
    model='sphere',
    texture=load_texture('assets/sky.jpg'),
    scale=500,
    double_sided=True
)

hand = Entity(              
    parent=camera.ui,
    model='assets/block',
    texture=blocks[t],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

def update():                                # gets called after every frame 
    if held_keys['right shift down'] or held_keys['left shift down']:   # ex right shift down , left mouse down 
        save()
        sound.play()

    elif held_keys['left mouse'] or held_keys['right mouse']:
        sound.play()
        hand.position = Vec2(0.4, -0.5)
        
    else:
        hand.position = Vec2(0.6, -0.6)

def save():
    f = open("pos.txt","w")
    f.write(str(pos))                                # saves the game (saves the dict format to save the build)
    f = open("tex.txt","w")
    f.write(str(tex))
    f.close() 

class Block(Button):                                # constructor to create objects i.e. blocks
    def __init__(self, position=(0, 0, 0), texture='assets/grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5)
    

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':                        # initiates when left mouse button is clicked
                Block(position=self.position + mouse.normal, texture=blocks[t])
                pos.append(self.position+mouse.normal)
                tex.append(self.texture+mouse.normal)

                save()
            elif key == 'right mouse down':                     # initiates when right mouse buttion is clicked
                
                if self.position in pos : 
                    ind = pos.index(self.position)
                    pos.remove(self.position)
                    tex.pop(ind)
                
                destroy(self)



surf = [1]*35 + [2]*10 + [3]*5                                  # defining probabilty list for land height

for z in range(50):                                             # setting up the world 50x50
    for x in range(50):
        k = r.choice(surf)          # choose a random element from surf (probabilty density for slope)
        
        for p in range(k):

            if p==0 : tr = r.choice([1,5,3,2])                   # initializing textures for ground
            
            else : tr= r.choice([1,3,4])                         # initializing textures for blocks other than ground
            
            block = Block(position=(x, p, z),texture=blocks[tr])     # creating the block
            pos.append((x,p,z))
            tex.append(blocks[t])



player = FirstPersonController()

app.run()
