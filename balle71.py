import pyxel, random

# défini les 
config = { 
    'taille_x' : 152, \
    'taille_y' : 152, \
    'titre' : 'casse briques', \
    'plateau_w' : 14, \
    'plateau_h' : 3,  \
    'vies' : 20, \
    'rayon_balle': 2, \
    'vitesse_max' : 15, \
    'niveau_max' : 3,
    'score' : 0
}
# défini la taille de la fenêtre et son titre
pyxel.init(config['taille_x'], config['taille_y'], title=config['titre'])

# ----------- Niveau ---------------------------
niveau = 1
temps = 1

# ----------- Plateau --------------------------
# position initiale du plateau
# (origine des positions : milieu du tiers inférieur)
plateau_x = 76
plateau_y = 140

def plateau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < config['taille_x'] - config['plateau_w']):
            x = x + 2
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - 2
    return x, y

def plateau_collision(x, y, rayon_balle):
    # il y a 3 sections sur un plateau: retourne 1, 2, 3 en fonction de là où ça rebondit

    if (y + rayon_balle >= plateau_y) and (y - rayon_balle < plateau_y + config['plateau_h']):
        if (x + rayon_balle >= plateau_x) and (x - rayon_balle < plateau_x + (config['plateau_w'] // 3) ):
            # rebond sur le 1er tiers du plateau
            return 1

        elif (x + rayon_balle >= plateau_x) and (x - rayon_balle < plateau_x + (2*config['plateau_w'] // 3) ):
            # rebond sur le milieu du plateau
            return 2

        elif (x + rayon_balle >= plateau_x) and (x - rayon_balle < plateau_x + config['plateau_w']):
            # rebond sur le dernier tiers du plateau
            return 3

    # pas de rebond
    return 0



# --------- Briques ---------------------------
def niveau_generation(niveau=1):
    tab = []
    # on a 3 types de briques : 
    # - les "faciles" : en un coup, elles sont détruites
    # - les "résistantes" : il faut plusieurs coups pour les détruire
    # - les "explosives" : si on les touche, ça fait tout sauter ! Bingo !
    if (niveau == 1):
        tab.append({ 'x' : 20, 'y' : 10, 'w' : 30, 'h' : 3, 'type' : 'facile', 'vie' : 1, 'couleur' : 3})
        tab.append({ 'x' : 60, 'y' : 10, 'w' : 30, 'h' : 3, 'type' : 'facile', 'vie' : 1, 'couleur' : 3})

    elif (niveau == 2):
        tab.append({ 'x' : 20, 'y' : 10, 'w' : 30, 'h' : 3, 'type' : 'resistante', 'vie' : 3, 'couleur' : 4})
        tab.append({ 'x' : 20, 'y' : 30, 'w' : 30, 'h' : 3, 'type' : 'facile', 'vie' : 3, 'couleur' : 3})
        tab.append({ 'x' : 100, 'y' : 10, 'w' : 30, 'h' : 3, 'type' : 'facile', 'vie' : 3, 'couleur' : 3})
        tab.append({ 'x' : 100, 'y' : 30, 'w' : 30, 'h' : 3, 'type' : 'resistante', 'vie' : 3, 'couleur' : 4})

    elif (niveau == 3):
        tab.append({ 'x' : 30, 'y' : 10, 'w' : 20, 'h' : 5, 'type' : 'explosion', 'vie' : 5, 'couleur': 5})
        tab.append({ 'x' : 70, 'y' : 10, 'w' : 30, 'h' : 3, 'type' : 'resistante', 'vie' : 3, 'couleur' : 4})
        tab.append({ 'x' : 110, 'y' : 10, 'w' : 30, 'h' : 3, 'type' : 'resistante', 'vie' : 1, 'couleur' : 3})


    return tab

tableau = niveau_generation(niveau)  

def brique_explosion():
    # lors d'une explosion, toutes les briques explosent !
    for brique in tableau:
        brique['vie'] = 0
    global config
    config['score'] = config['score'] + 100
       

def brique_collision(x, y, r):
    # dit si le cercle en (x, y), rayon r touche une brique du tableau
    for brique in tableau:
        if (brique['vie'] > 0) and (x + r > brique['x']) and (x -r < brique['x'] + brique['w']) \
            and (y + r > brique['y']) and (y - r < brique['y'] + brique['h']):

            # destruction progressive de la brique
            # les briques faciles sont détruites en 1 coup
            brique['vie'] = brique['vie'] - 1
            global config
            config['score'] = config['score'] + 50
            
            if brique['type'] == 'explosion':
                brique_explosion()

            return True

    return False


# ----------- Balle ----------------------------
def balle_generation():
    # création d'une nouvelle balle, en haut, au milieu
    x = config['taille_x'] // 2
    y = 15

    # angle aléatoire - les angles trop horizontaux ne sont pas intéressants
    # à jouer, on les exclut
    angle_initial = random.randint(30, 150)

    return x, y, angle_initial

balle_x, balle_y, balle_angle = balle_generation()  

def angles_horizontaux(angle):
    # on exclut les angles trop horizontaux
    if angle < 30:
        angle = 30

    if angle > 150 and angle < 180:
        angle = 150

    if angle >= 180 and angle < 210:
        angle = 210

    if angle > 330:
        angle = 330

    return angle

def balle_deplacement(x, y, angle, x_max = 152, y_max = 140):
    global config

    # la vitesse augmente avec le temps 
    vitesse_initiale = niveau + 2
    vitesse = vitesse_initiale + pyxel.floor(temps / 50000)
    if (vitesse > config['vitesse_max']):
        vitesse = config['vitesse_max']

    x = pyxel.floor(x + vitesse * pyxel.cos(angle))
    y = pyxel.floor(y + vitesse * pyxel.sin(angle))

    # rebond sur le plateau
    type_collision = plateau_collision(x, y, config['rayon_balle'])
    if type_collision > 0:
        angle = 360 - angle
        y = plateau_y - config['plateau_h']
        print(f"rebond sur plateau: angle={angle}")
        if type_collision == 1:
            angle = angle - 20
        elif type_collision == 3:
            angle = angle + 20

    elif brique_collision(x, y, config['rayon_balle']):
        angle = 360 - angle
        print(f"rebond sur une brique: angle={angle}")

    if (y >= y_max):
        # la balle a dépassé le plateau ! 
        # on pert une vie, et on ré-initialise la balle
        config['vies'] = config['vies'] - 1
        x, y, angle = balle_generation()

    elif (y < 0):
        # rebond sur le haut
        angle = 360 - angle
        y = 0
        print(f"rebond sur le haut: {x}, {y}, angle={angle}")

    elif (x < 0):
        if (angle < 180):
            # rebond sur le côté gauche du tableau
            angle = 180 - angle
        else: 
            angle = 180 + angle
        x = 0
        print(f"rebond gauche: {x}, {y}, angle={angle}")

    elif (x >= x_max):
        # rebond sur le côté droit du tableau
        if (angle < 180):
            angle = 180 - angle
        else:
            angle = 360 - (angle - 180)
        x = x_max
        print(f"rebond droit: {x}, {y}, angle={angle}")

    angle = angles_horizontaux(angle)
    return x, y, angle

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y
    global balle_x, balle_y, balle_angle, temps
    # mise à jour de la position du plateau
    plateau_x, plateau_y = plateau_deplacement(plateau_x, plateau_y)

    # la vitesse de la balle augmente avec le temps
    temps = temps + 1
  
        
    # mise à jour de la position de la balle
    balle_x, balle_y, balle_angle = balle_deplacement(balle_x, balle_y, balle_angle)
    print(f"Temps:{temps} Balle: ({balle_x}, {balle_y}), Plateau: ({plateau_x},{plateau_y}), angle={balle_angle}")


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    if (config['vies'] < 1):
        # jeu terminé
        pyxel.text(50, 50, "GAME OVER", 7)   
        pyxel.text(40, 60, "Appuyer sur ENTREE ", 7)
        pyxel.text(50, 80, "BRAVOOOOOOOOO !", 7)
        if pyxel.btn(pyxel.KEY_RETURN):
            pyxel.quit()

    else:
        # plateau (rectangle 14x3)
        pyxel.rect(plateau_x, plateau_y, config['plateau_w'], config['plateau_h'], 1)
        pyxel.text(110, 10,"vies : %s " %str(config['vies']), 7)
        pyxel.text(110, 20,"score : %s " %str(temps + config['score']), 7)

        # balle (cercle)
        pyxel.circ(balle_x, balle_y, config['rayon_balle'], 2)

        # briques
        niveau_termine = True
        global tableau
        for b in tableau:
            if (b['vie'] > 0):
                pyxel.rect(b['x'], b['y'], b['w'], b['h'], b['couleur'])
                niveau_termine = False

        if (niveau_termine):
            global niveau
            pyxel.text(50, 50, "NIVEAU %s TERMINE" % niveau, 7)   
            pyxel.text(40, 60, "Appuyer sur ENTREE ", 7)  
            pyxel.text(50, 80, "Continue !", 7) 
            if pyxel.btn(pyxel.KEY_RETURN):
                niveau = niveau + 1
                if niveau > config['niveau_max']:
                    # on a tout gagné                 
                    pyxel.quit()
                else:
                    # passage au niveau suivant
                    tableau = niveau_generation(niveau) 
                
        
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.DM_casse_brique.balle13
pyxel.run(update, draw)
