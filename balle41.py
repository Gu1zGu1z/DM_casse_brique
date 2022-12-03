import pyxel

# taille de la fenetre 152x152 pixels
# ne pas modifier
pyxel.init(152, 152, title="casse brique")

# position initiale du vaisseau
# (origine des positions : milieu du tiers inférieur)
plateau_x = 76
plateau_y = 140
balle = False
vie = 3

def plateau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 144) :
            x = x + 2
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - 2
    return x, y

# position initiale de la balle
# (origine des positions : au-dessus du plateau)
balle_x = 76
balle_y = 120

def balle_deplacement(x, y):
    if balle_x = 0:
        x = x + 1
    if balle_x = 158:
        x = x - 1
    if balle_y = 0:
        y = y + 1
    if balle_y = 148:
        y = y - 1
        
        
    return x, y
    


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y, balle_x, balle_y

    # mise à jour de la position du vaisseau
    plateau_x, plateau_y = plateau_deplacement(plateau_x, plateau_y)
    # mise à jour de la position de la balle
    balle_x, balle_y = balle_deplacement(balle_x, balle_y)
    

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # vaisseau (rectangle 8x3)
    pyxel.rect(plateau_x, plateau_y, 8, 3, 1)
    # balle ( carrée 8x8 )
    pyxel.circ(balle_x, balle_y, rayon, 2)
    pyxel.text(200, 10,"score : %s " % str(score), 7)
    pyxel.text(200, 20,"vie : %s " %str(vie), 7)
    
    
        
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.DM_casse_brique.balle13
pyxel.run(update, draw)
