import pyxel, random

# taille de la fenetre 152x152 pixels
pyxel.init(152, 152, title="casse brique")

# position initiale du vaisseau
# (origine des positions : milieu du tiers inférieur)
plateau_x = 76
plateau_y = 140
vie = 3
blocs_liste = []

def plateau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 144) :
            x = x + 2
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - 2
    return x, y


def blocs_creation(blocs_liste):
    """création des blocs"""

    # un ennemi par seconde
    if (pyxel.frame_count % 30 == 0):
        blocs_liste.append([random.randint(0, 120), 0])
    return blocs_creation

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y, blocs_liste

    # mise à jour de la position du plateau
    plateau_x, plateau_y = plateau_deplacement(plateau_x, plateau_y)
    
    # creation des blocs
    blocs_liste = blocs_creation(blocs_liste)
   

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # vaisseau (rectangle 8x3)
    pyxel.rect(plateau_x, plateau_y, 8, 3, 1 )
    pyxel.text(100, 20,"vie : %s " %str(vie), 7)
    # blocs
    for blocs in blocs_liste:
        pyxel.rect(blocs[0], blocs[1], 8, 8, 8)   
    
    
        
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.DM_casse_brique.balle13
pyxel.run(update, draw)
