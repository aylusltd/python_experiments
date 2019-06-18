import constants, sprites
listeners = []
def key_listener(key = None, keycode = None):
    def faux_wrapper(l):
        def wrapper(*args, **kwargs):
            s = args[0]
            e = args[1]
            if ((keycode is None or keycode == e.keycode) and 
                (key is None or key == e.char)):
                return l(*args, **kwargs)
            else:
                return None
        listeners.append(wrapper)
        return wrapper
    return faux_wrapper

def spear_check(l):
    def wrapper(*args, **kwargs):
        s = args[0]
        e = args[1]
        if s.inventory["spears"]["qty"] <= 0:
            return None
        else:
            s.inventory["spears"]["qty"] -=1
            s.update_inventory()
            return l(s,e)
    return wrapper

def move_tux(l):
    def wrapper(*args, **kwargs):
        s=args[0]
        grid = s.screen.grid
        grid[s.tux.row][s.tux.column].occupied = False
        grid[s.tux.row][s.tux.column].has_tux = False
        l(*args, **kwargs)
        grid[s.tux.row][s.tux.column].occupied = True
        grid[s.tux.row][s.tux.column].has_tux = True
    return wrapper


@key_listener(key="a")
@spear_check
def spear_left(s,e):
    y = s.tux.row
    x = s.tux.column
    s = sprites.Spear(s, d=90, x=x, y=y)
    # print "spear_left"

@key_listener(key="d")
@spear_check
def spear_right(s,e):
    # print "spear_right"
    y = s.tux.row
    x = s.tux.column
    s = sprites.Spear(s, d=270, x=x, y=y)
    # print "spear_right"

@key_listener(key="w")
@spear_check
def spear_up(s,e):
    y = s.tux.row
    x = s.tux.column
    s = sprites.Spear(s, d=0, x=x, y=y)
    # print "spear_up"

@key_listener(key="x")
@spear_check
def spear_down(s,e):
    y = s.tux.row
    x = s.tux.column
    s = sprites.Spear(s, d=180, x=x, y=y)
    # print "spear_down"

@key_listener(key="h")
def harvest(s,e):
    r = s.tux.row
    c = s.tux.column
    g = s.screen.grid
    if g[r][c].has_tree:
        s.inventory["wood"]["qty"]+=10
        g[r][c].has_tree=False
        s.screen.canvas.delete(g[r][c].sprites["tree_sprite"])
    elif g[r][c].has_rock:
        s.inventory["rock"]["qty"]+=10
        g[r][c].has_rock=False
        s.screen.canvas.delete(g[r][c].sprites["rock_sprite"])
    s.update_inventory()    
    # print "harvest"

@key_listener(key="r")
def craft_spear(s,e):
    key = "spears"
    ingredients = ["wood", "rock"]
    inventory = s.inventory
    if has_ingredients(ingredients, inventory):
        consume_ingredients(ingredients, inventory)
        inventory[key]["qty"]+=1
    s.update_inventory()    
    # print "craft spear"

@key_listener(key="b")
def craft_brick(s,e):
    key = "brick"
    ingredients = ["rock", "rock"]
    inventory = s.inventory
    if has_ingredients(ingredients, inventory):
        consume_ingredients(ingredients, inventory)
        inventory[key]["qty"]+=1
    s.update_inventory()    
    # print "craft brick"

@key_listener(key="l")
def craft_wall(s,e):
    key = "wall"
    ingredients = ["brick", "brick", "brick", "brick", "brick"]
    inventory = s.inventory
    if has_ingredients(ingredients, inventory):
        consume_ingredients(ingredients, inventory)
        inventory[key]["qty"]+=1
    s.update_inventory()    
    # print "craft wall"
@key_listener(key="p")
def place_wall(s,e):
    key = "wall"
    ingredients = ["wall"]
    inventory = s.inventory
    r = s.tux.row
    c = s.tux.column
    g = s.screen.grid
    square = g[r][c]
    if has_ingredients(ingredients, inventory):
        consume_ingredients(ingredients, inventory)
        square.add_feature(feature="wall", app=s, passable=False)
        s.update_inventory()
    # print "place wall"
@key_listener(key="z")
def destroy_wall(s,e):
    key = "wall"
    ingredients = ["wall"]
    inventory = s.inventory
    screen = s.screen
    r = s.tux.row
    c = s.tux.column
    g = s.screen.grid
    square = g[r][c]
    touching_wall = screen.neighbor_has(feature=key, i=r, j=c)
    if touching_wall:
        s.action = "destroy wall"
    # print "destroying wall"

@key_listener(key="f")
def catch_fish(s,e):
    key = "fish"
    # ingredients = ["fish"]
    # inventory = s.inventory
    # s.config(cursor='circle red red')
    screen = s.screen
    r = s.tux.row
    c = s.tux.column
    g = s.screen.grid
    square = g[r][c]
    touching_wall = screen.neighbor_has(feature=key, i=r, j=c)
    if touching_wall:
        s.action = "catch fish"
    # print "destroying wall"

def has_ingredients(ingredients, inventory):
    t={}
    for i in inventory:
        t[i]=inventory[i]["qty"]
    for ingredient in ingredients:
        if t[ingredient] < 1:
            return False
        t[ingredient]-=1
    return True

def consume_ingredients(ingredients, inventory):
    for ingredient in ingredients:
        inventory[ingredient]["qty"]-=1


@key_listener(keycode=8320768)
@move_tux
def move_up(s,e):
    g=s.g
    if s.tux.row > 0:
            if s.screen.grid[s.tux.row-1][s.tux.column].passable:
                s.screen.canvas.move(s.tux.sprite,0,-g)
                s.tux.row-=1

@key_listener(keycode=8255233)
@move_tux
def move_down(s,e):
    g=s.g
    if s.tux.row < s.max_row:
        if s.screen.grid[s.tux.row+1][s.tux.column].passable:
            s.screen.canvas.move(s.tux.sprite,0,g)
            s.tux.row+=1

@key_listener(keycode=8124162)
@move_tux
def move_left(s,e):
    g=s.g
    if s.tux.column > 0:
        if s.screen.grid[s.tux.row][s.tux.column-1].passable:
            s.screen.canvas.move(s.tux.sprite,-g,0)
            s.tux.column-=1

@key_listener(keycode=8189699)
@move_tux
def move_right(s,e):
    g=s.g
    if s.tux.column < s.max_column:
        if s.screen.grid[s.tux.row][s.tux.column+1].passable:
            s.screen.canvas.move(s.tux.sprite,g,0)
            s.tux.column+=1

def on_keypress(s, event):
    h = constants.bounds["y"][1]
    w = constants.bounds["x"][1]
    g = constants.grid_size
    c = s.screen.canvas
    p=c.coords(s.tux.sprite)

    current_row = int((p[1]-4)/g)
    current_column = int((p[0]-4)/g)
    s.tux.row=current_row
    s.tux.column=current_column
    s.max_row = int(h/g)-1
    s.max_column = int(w/g)-1
    s.screen.grid[current_row][current_column].occupied = False
    
    for l in listeners:
            l(s,event)
    s.screen.grid[s.tux.row][s.tux.column].occupied = True
    # s.root.after(constants.INTERVAL*2, s.monsters_move)