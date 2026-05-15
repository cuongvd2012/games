import pygame, pickle, math
pygame.init()
pygame.font.init()
w=pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Sokomath")
next_free=1
lvs={}
objlvs={}
modified={}
animation={}
class lvreference:
    def __init__(self, name):
        if name in lvs:
            self.id=name
        else:
            raise NameError
class lv:
    def __init__(self, dimensions, name, color=(32, 90, 189)):
        self.dimensions=dimensions
        self.id=name
        self.obj={}
        self.obj2={}
        self.color=color
    def add(self, typee, pos, id=None):
        global next_free, objlvs
        if id is None: id=next_free
        if id==next_free: next_free+=1
        self.obj[pos]=(id, typee)
        self.obj2[id]=(pos, typee)
        objlvs[id]=self.id
        return id
    def remove(self, id):
        self.obj.pop(self.obj2[id][0])
        self.obj2.pop(id)
        objlvs.pop(id)
        animation[id]=None
        animation.pop(id)
    def teleport(self, id, newpos):
        pos=self.obj2[id][0]
        typee=self.obj2[id][1]
        self.obj[newpos]=self.obj[pos]
        self.obj.pop(pos)
        self.obj2[id]=(newpos, typee)
    def copy(self):
        lvlcopy=lv(self.dimensions, self.id, self.color)
        for pos, (id, typee) in self.obj.items():
            lvlcopy.add(typee, pos, id=id)
        return lvlcopy
    def gridify(self):
        grid = [[None for i in range(self.dimensions[0])] for j in range(self.dimensions[1])]
        for item in self.obj.items():
            grid[item[0][1]][item[0][0]] = item[1]
        return grid
class obj:
    def __init__(self, typee, value=None):
        self.type=typee
        self.value=value
def newlevel(dimensions, name, color=(200, 200, 200)):
    lvs[name]=lv(dimensions, name, color)
    return lvs[name]
def drawlevel(name, x, y, scaley, frame=0):
    tilesizey=scaley/lvs[name].dimensions[1]
    tilesizex=tilesizey
    scalex=scaley*lvs[name].dimensions[0]/lvs[name].dimensions[1]
    r=pygame.Rect(x, y, scalex, scaley)
    r.center=(w.get_width()/2, w.get_height()/2)
    pygame.draw.rect(w, lvs[name].color, r)
    x=r.x
    y=r.y
    font=pygame.font.SysFont(None, int(tilesizex*1.6))
    font2=pygame.font.SysFont(None, int(tilesizex*0.5))
    for pos, (id, typee) in lvs[name].obj.items():
        if typee.type=="wall":
            pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(x+tilesizex*pos[0]-tilesizex*0.05), math.floor(y+tilesizey*pos[1]-tilesizey*0.05), math.ceil(tilesizex+tilesizex*0.1), math.ceil(tilesizey+tilesizey*0.1)))
    for pos, (id, typee) in lvs[name].obj.items():
        if typee.type=="wall":
            pygame.draw.rect(w, (min(int(lvs[name].color[0]*1.4), 255), min(int(lvs[name].color[1]*1.4), 255), min(int(lvs[name].color[2]*1.4), 255)),
                             pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey)))
        elif typee.type=="win":
            pygame.draw.circle(w, (36, 255, 76), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex*0.4)
            surf=font2.render("win", False, (0, 0, 0))
            npos=(x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
        elif typee.type=="lock":
            pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2))
            surf=font.render(typee.value, False, (0, 0, 0))
            npos=(x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
        else:
            surf=font.render(typee.value, False, (255, 255, 255))
            surf2=font.render(typee.value, False, (0, 0, 0))
            npos=(x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2+tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2-tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2+tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2-tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2+tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2+tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2-tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2-tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2-tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2+tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2+tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2-tilesizey/30))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
    pygame.draw.rect(w, (0, 0, 0), pygame.Rect(x, y, scalex, scaley), width=2)
def push(id, dxy, max_depth=99, typpe=None):
    if id==-1: return True
    if max_depth<1: return False
    dx=dxy[0]
    dy=dxy[1]
    lvv=lvs[objlvs[id]]
    typeee=lvv.obj2[id][1]
    if typeee.type=="wall": return False
    pos, typeeee=lvv.obj2[id]
    if typpe is None: typpe=typeeee
    newpos=(pos[0]+dx, pos[1]+dy)
    (nid, typee)=lvv.obj.get(newpos, (-1, ""))
    if newpos[0]<0 or newpos[0]>=lvv.dimensions[0] or newpos[1]<0 or newpos[1]>=lvv.dimensions[1]:
        return False
    if typee!="" and typee.type!=typpe.type: return False
    pushh=nid==-1
    if not pushh: pushh=push(nid, dxy, max_depth=max_depth-1, typpe=typpe)
    if pushh:
        lvv.teleport(id, newpos)
        modified[pos]=True
        modified[newpos]=True
        animation[nid]=("push", dxy)
        return True
    return False
def parse(tokens):
    i = 0
    def peek():
        return tokens[i] if i < len(tokens) else ""
    def eat():
        nonlocal i
        i += 1
        return tokens[i-1] if i-1 < len(tokens) else ""
    def parse_expr():
        return parse_add()
    def parse_add():
        result = parse_mul()
        cont = True
        while True:
            cont = False
            if peek() == "+":
                eat()
                cont = True
                res = parse_mul()
                result[0] += res[0]
                result[1] = result[1] and res[1]
            if peek() == "-":
                eat()
                cont = True
                res = parse_mul()
                result[0] -= res[0]
                result[1] = result[1] and res[1]
            if not cont:
                break
        return result
    def parse_mul():
        result = parse_num()
        cont = True
        while True:
            cont = False
            if peek() == "*":
                eat()
                cont = True
                res = parse_num()
                result[0] *= res[0]
                result[1] = result[1] and res[1]
            if not cont:
                break
        return result
    def parse_num():
        num = 0
        cont = True
        valid = False
        if peek() == "(":
            eat()
            num = parse_expr()
            if peek() == ")":
                eat()
                return num
        while True:
            cont = False
            p = peek()
            if p in "0123456789" and p != "":
                cont = True
                num *= 10
                num += int(eat())
                valid = True
            if not cont:
                break
        return [num, valid]
    return parse_expr()
        
def checkeq(lvv):
    grid = lvv.gridify()
    tokens = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "+", "-", "*",
              "(", ")"]
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c is None: continue
            if c[1].value == "=":
                direction = []
                if i > 0 and grid[i-1][j] is not None:
                    direction.append((0, -1))
                if j > 0 and grid[i][j-1] is not None:
                    direction.append((-1, 0))
                for d in direction:
                    parts = []
                    pos = [j+d[0],i+d[1]]
                    while 0 <= pos[0] < lvv.dimensions[0] and 0 <= pos[1] < lvv.dimensions[1] and grid[pos[1]][pos[0]] is not None and grid[pos[1]][pos[0]][1].value in tokens:
                        parts = [grid[pos[1]][pos[0]]]+parts
                        pos = [pos[0]+d[0],pos[1]+d[1]]
                    parts = [part[1].value for part in parts]
                    if parts:
                        print(parts)
                        result = parse(parts)
                        print(result)
                        if not result[1]:
                            continue
                        pieces = list(str(result[0]))
                        starting = [j-d[0],i-d[1]]
                        bsignal = False
                        for I in range(len(pieces)):
                            npos = [starting[0]-d[0]*I,starting[1]-d[1]*I]
                            if grid[npos[1]][npos[0]] is not None:
                                bsignal = True
                                break
                        if pieces == parts:
                            continue
                        if bsignal:
                            continue
                        for I in range(len(pieces)):
                            npos = [starting[0]-d[0]*I,starting[1]-d[1]*I]
                            lvv.add(obj("push", pieces[I]), tuple(npos))
                        for I in range(len(parts)):
                            npos = [j+d[0]*(I+1),i+d[1]*(I+1)]
                            lvv.remove(grid[npos[1]][npos[0]][0])
                            
                
                


def cancel(lvv):
    removee=set()
    for pos, (idd, typee) in list(lvv.obj.items()):
        if typee.type=="lock":
            x, y=pos
            next=[(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            for newpos in next:
                if newpos in lvv.obj:
                    nid, typeee=lvv.obj[newpos]
                    if typeee.type=="push" and typeee.value==typee.value:
                        if idd!=player: removee.add(idd)
                        if nid!=player: removee.add(nid)
    for iidd in removee:
        lvv.remove(iidd)
lvvll=None
player=-1
def save(file):
    save={
        "level": lvvll,
        "objlvs": objlvs,
        "next_free": next_free,
        "player_id": player
    }
    with open(file, "wb") as f: pickle.dump(save, f)
def load(file):
    global lvvll, objlvs, next_free, player
    with open(file, "rb") as f: load=pickle.load(f)
    lvvll=load["level"]
    objlvs=load["objlvs"]
    next_free=load["next_free"]
    player=load["player_id"]
    lvs[lvvll.id]=lvvll
def createlv():
    global player, lvvll
    lvvll=newlevel((11, 9), "root", color=(150, 0, 214))
    for i in range(11):
        lvvll.add(obj("wall"), (i, 0))
        lvvll.add(obj("wall"), (i, 8))
    for i in range(1, 8):
        lvvll.add(obj("wall"), (0, i))
        lvvll.add(obj("wall"), (10, i))
    player=lvvll.add(obj("push", "="), (1, 7))
    lvvll.add(obj("wall"), (1, 5))
    lvvll.add(obj("wall"), (2, 5))
    lvvll.add(obj("wall"), (3, 5))
    lvvll.add(obj("wall"), (4, 5))
    lvvll.add(obj("wall"), (4, 4))
    lvvll.add(obj("wall"), (4, 2))
    lvvll.add(obj("wall"), (8, 2))
    lvvll.add(obj("wall"), (9, 2))
    lvvll.add(obj("wall"), (4, 1))
    lvvll.add(obj("wall"), (4, 7))
    lvvll.add(obj("push", "1"), (2, 6))
    lvvll.add(obj("push", "2"), (2, 2))
    lvvll.add(obj("push", "+"), (3, 2))
    lvvll.add(obj("push", "2"), (6, 4))
    lvvll.add(obj("push", "3"), (8, 5))
    lvvll.add(obj("lock", "1"), (4, 6))
    lvvll.add(obj("lock", "2"), (4, 3))
    lvvll.add(obj("lock", "5"), (8, 1))
    lvvll.add(obj("win"), (9, 1))
createlv(); save("level.lv")
#load("level.lv")
lvprestates=[]
#lvprestates.append(lvvll.copy())
clock=pygame.time.Clock()
x=True
while x:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: x=False
        elif event.type==pygame.KEYDOWN:
            modified={}
            animation={}
            if event.key==pygame.K_UP:
                push(player, (0, -1))
                checkeq(lvvll)
                cancel(lvvll)
                #lvprestates.append(lvvll.copy())
            elif event.key==pygame.K_DOWN:
                push(player, (0, 1))
                checkeq(lvvll)
                cancel(lvvll)
                #lvprestates.append(lvvll.copy())
            elif event.key==pygame.K_RIGHT:
                push(player, (1, 0))
                checkeq(lvvll)
                cancel(lvvll)
                #lvprestates.append(lvvll.copy())
            elif event.key==pygame.K_LEFT:
                push(player, (-1, 0))
                checkeq(lvvll)
                cancel(lvvll)
                #lvprestates.append(lvvll.copy())
            #elif event.key==pygame.K_z:
                #if len(lvprestates)>1:
                    #objlvs={}
                    #lvvv=lvprestates[-2].copy()
                    #lvprestates.pop()
                    #lvs[lvvll.id]=lvvll
    w.fill((0, 0, 0))
    fit=min(w.get_width(), w.get_height())*0.8
    drawlevel(objlvs[player], (w.get_width()-fit)/2, (w.get_height()-fit)/2, fit)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
