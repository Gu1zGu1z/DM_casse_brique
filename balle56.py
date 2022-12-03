import pyxel, random

# taille de la fenetre 152x152 pixels
pyxel.init(152, 152, title="casse brique")

# position initiale du vaisseau
# (origine des positions : milieu du tiers inférieur)
plateau_x = 76
plateau_y = 140
vies = 3


def plateau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 140) :
            x = x + 2
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - 2
    return x, y


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y

    # mise à jour de la position du plateau
    plateau_x, plateau_y = plateau_deplacement(plateau_x, plateau_y)
    

   

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # vaisseau (rectangle 8x3)
    pyxel.rect(plateau_x, plateau_y, 12, 3, 1 )
    pyxel.text(110, 10,"vie : %s " %str(vies), 7)
   
    
    
        
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.DM_casse_brique.balle13
pyxel.run(update, draw)
