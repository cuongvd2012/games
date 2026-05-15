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
bgobjs={"win", "lv"}
lvhistory=["w1"]
class lv:
    def __init__(self, dimensions, name, color=(32, 90, 189)):
        self.dimensions=dimensions
        self.id=name
        self.obj={}
        self.obj2={}
        self.bg={}
        self.bg2={}
        self.color=color
    def add(self, typee, pos, id=None):
        global next_free, objlvs
        if id is None: id=next_free
        if id==next_free: next_free+=1
        if typee.type in bgobjs:
            self.bg[pos]=(id, typee)
            self.bg2[id]=(pos, typee)
        else:
            self.obj[pos]=(id, typee)
            self.obj2[id]=(pos, typee)
        objlvs[id]=self.id
        return id
    def remove(self, id):
        try:
            self.obj.pop(self.obj2[id][0])
            self.obj2.pop(id)
        except Exception:
            self.bg.pop(self.obj2[id][0])
            self.bg2.pop(id)
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
    font3=pygame.font.SysFont(None, int(tilesizex*0.9))
    for pos, (id, typee) in lvs[name].obj.items():
        if typee.type=="wall":
            pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(x+tilesizex*pos[0]-tilesizex*0.05), math.floor(y+tilesizey*pos[1]-tilesizey*0.05), math.ceil(tilesizex+tilesizex*0.1), math.ceil(tilesizey+tilesizey*0.1)))
    for pos, (id, typee) in lvs[name].bg.items():
        if typee.type=="win":
            pygame.draw.circle(w, (36, 255, 76), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex*0.4)
            surf=font2.render("win", False, (0, 0, 0))
            npos=(x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
        elif typee.type=="lv":
            pygame.draw.circle(w, (0, 0, 0), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex*0.4, width=int(tilesizex*0.15))
            pygame.draw.circle(w, (255, 255, 255), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex*0.4, width=int(tilesizex*0.1))
            surf=font3.render(typee.value[1], False, (255, 255, 255))
            surf2=font3.render(typee.value[1], False, (0, 0, 0))
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
    for pos, (id, typee) in lvs[name].obj.items():
        if typee.type=="wall":
            pygame.draw.rect(w, (min(int(lvs[name].color[0]*1.4), 255), min(int(lvs[name].color[1]*1.4), 255), min(int(lvs[name].color[2]*1.4), 255)),
                             pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey)))
        elif typee.type=="lock":
            pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2))
            surf=font.render(typee.value, False, (0, 0, 0))
            npos=(x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
        elif typee.type=="levellock":
            pygame.draw.rect(w, (255, 0, 0), pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2))
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
    pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(x+tilesizex*player[0]), math.floor(y+tilesizey*player[1]), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2), width=int(tilesizex*0.1))
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
    (nid, typee)=lvv.obj.get(newpos, (-1, None))
    if newpos[0]<0 or newpos[0]>=lvv.dimensions[0] or newpos[1]<0 or newpos[1]>=lvv.dimensions[1]:
        return False
    if typee!=None and typee.type!=typpe.type: return False
    pushh=nid==-1
    if not pushh: pushh=push(nid, dxy, max_depth=max_depth-1, typpe=typpe)
    if pushh:
        lvv.teleport(id, newpos)
        modified[pos]=True
        modified[newpos]=True
        animation[nid]=("key", dxy)
        return True
    return False
def checkeq(lvv):
    global player
    symbols=set("0123456789+-*")
    ops=set("+-*")
    dele=set()
    for pos in list(lvv.obj.keys()):
        idd, typee=lvv.obj[pos]
        if typee.value=="=":
            x, y=pos
            eq=[]
            iddd=[]
            xx=x-1
            satsat=False
            satsatsat=True
            while (xx, y) in lvv.obj and lvv.obj[(xx, y)][1].type==typee.type:
                iid, typeee=lvv.obj[(xx, y)]
                if typeee.value in symbols:
                    eq.insert(0, typeee.value)
                    iddd.insert(0, iid)
                    xx-=1
                    if typeee.value in ops and not satsat:
                        satsat=True
                        satsatsat=False
                    elif satsat and not satsatsat and typeee not in ops:
                        satsatsat=True
                else:
                    break
            if not eq: continue
            if not satsatsat: continue
            if not satsat: continue
            eq="".join(eq)
            try:
                ans=str(eval(eq))
                sat=True
                for i in range(len(ans)):
                    neepos=(x+i+1, y)
                    if neepos in lvv.obj or neepos[0]>=lvv.dimensions[0]:
                        sat=False
                        break
                if sat:
                    for eid in iddd:
                        print(lvv.obj2[eid][0])
                        if lvv.obj2[eid][0]!=player: dele.add(eid)
                    if pos!=player: dele.add(idd)
                    for i, char in enumerate(ans):
                        newpos=(x+i+1, y)
                        nid=lvv.add(obj(typee.type, char), newpos)
                        animation[nid]=("key", (1, 0))
            except Exception:
                continue
    for pos in list(lvv.obj.keys()):
        idd, typee=lvv.obj[pos]
        if typee.value=="=":
            x, y=pos
            eq=[]
            iddd=[]
            yy=y-1
            satsat=False
            satsatsat=True
            while (x, yy) in lvv.obj and lvv.obj[(x, yy)][1].type==typee.type:
                iid, typeee=lvv.obj[(x, yy)]
                if typeee.value in symbols:
                    eq.insert(0, typeee.value)
                    iddd.insert(0, iid)
                    yy-=1
                    if typeee.value in ops and not satsat:
                        satsat=True
                        satsatsat=False
                    elif satsat and not satsatsat and typeee not in ops:
                        satsatsat=True
                else:
                    break
            if not eq: continue
            if not satsatsat: continue
            if not satsat: continue
            eq="".join(eq)
            try:
                ans=str(eval(eq))
                sat=True
                for i in range(len(ans)):
                    neepos=(x, y+i+1)
                    if neepos in lvv.obj or neepos[0]>=lvv.dimensions[0]:
                        sat=False
                        break
                if sat:
                    for eid in iddd:
                        if lvv.obj2[eid][0]!=player: dele.add(eid)
                    if pos!=player: dele.add(idd)
                    for i, char in enumerate(ans):
                        newpos=(x, y+i+1)
                        nid=lvv.add(obj(typee.type, char), newpos)
                        animation[nid]=("key", (0, 1))
            except Exception:
                continue
    for idid in dele:
        lvv.remove(idid)
def cancel(lvv):
    removee=set()
    for pos, (idd, typee) in list(lvv.obj.items()):
        if typee.type=="lock":
            x, y=pos
            next=[(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            for newpos in next:
                if newpos in lvv.obj:
                    nid, typeee=lvv.obj[newpos]
                    if typeee.type=="key" and typeee.value==typee.value:
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
        "player": player
    }
    with open(file, "wb") as f: pickle.dump(save, f)
def load(file):
    global lvvll, objlvs, next_free, player
    with open(file, "rb") as f: load=pickle.load(f)
    lvvll=load["level"]
    objlvs=load["objlvs"]
    next_free=load["next_free"]
    player=load["player"]
    lvs[lvvll.id]=lvvll
def createlv():
    global player, lvvll
    lvvll=newlevel((12, 11), "root", color=(150, 0, 214))
    for i in range(12):
        lvvll.add(obj("wall"), (i, 0))
        lvvll.add(obj("wall"), (i, 10))
    for i in range(1, 10):
        lvvll.add(obj("wall"), (0, i))
        lvvll.add(obj("wall"), (11, i))
    for i in range(3, 12): lvvll.add(obj("wall"), (i, 7))
    lvvll.add(obj("wall"), (4, 1))
    lvvll.add(obj("wall"), (4, 2))
    lvvll.add(obj("wall"), (4, 3))
    lvvll.add(obj("wall"), (8, 1))
    lvvll.add(obj("wall"), (8, 2))
    lvvll.add(obj("wall"), (8, 3))
    lvvll.add(obj("wall"), (7, 3))
    lvvll.add(obj("wall"), (3, 8))
    lvvll.add(obj("wall"), (3, 9))
    lvvll.add(obj("win"), (7, 2))
    lvvll.add(obj("key", "+"), (1, 1))
    lvvll.add(obj("key", "2"), (2, 2))
    lvvll.add(obj("key", "3"), (2, 3))
    lvvll.add(obj("key", "4"), (4, 5))
    lvvll.add(obj("key", "="), (5, 5))
    lvvll.add(obj("key", "3"), (6, 5))
    lvvll.add(obj("key", "="), (7, 5))
    lvvll.add(obj("key", "4"), (8, 5))
    lvvll.add(obj("key", "4"), (2, 8))
    lvvll.add(obj("key", "3"), (9, 2))
    lvvll.add(obj("lock", "4"), (9, 3))
    lvvll.add(obj("lock", "4"), (10, 3))
    lvvll.add(obj("lock", "3"), (1, 7))
    lvvll.add(obj("lock", "2"), (2, 7))
    lvvll.add(obj("lock", "6"), (5, 3))
    lvvll.add(obj("lock", "5"), (5, 2))
    lvvll.add(obj("lock", "7"), (6, 3))
    lvvll.add(obj("lock", "9"), (6, 2))
    player=(1, 1)
#createlv(); save("w1-2.lv")
#load("level.lv")
load("w1.lv")
clock=pygame.time.Clock()
x=True
while x:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: x=False
        elif event.type==pygame.KEYDOWN:
            modified={}
            animation={}
            move=None
            if event.key==pygame.K_UP:
                move=(0, -1)
            elif event.key==pygame.K_DOWN:
                move=(0, 1)
            elif event.key==pygame.K_RIGHT:
                move=(1, 0)
            elif event.key==pygame.K_LEFT:
                move=(-1, 0)
            if move is not None:
                pp=lvvll.obj.get(player, (-1, None))
                if pp[0]!=-1 and pp[1].type!="wall":
                    push(pp[0], move)
                    try:
                        player=lvvll.obj2[pp[0]][0]
                    except KeyError:
                        player=(player[0]+move[0], player[1]+move[1])
                    checkeq(lvvll)
                    try:
                        player=lvvll.obj2[pp[0]][0]
                    except KeyError:
                        player=(player[0]+move[0], player[1]+move[1])
                    cancel(lvvll)
                    try:
                        player=lvvll.obj2[pp[0]][0]
                    except KeyError:
                        player=(player[0]+move[0], player[1]+move[1])
                else:
                    player=(player[0]+move[0], player[1]+move[1])
                    pp=lvvll.obj.get(player, (-1, None))
                    if pp[0]!=-1 and pp[1].type=="wall": player=(player[0]-move[0], player[1]-move[1])
            ppp=lvvll.bg.get(player, (-1, None))
            if ppp[0]!=-1:
                if ppp[1].type=="lv":
                    if event.key==pygame.K_SPACE:
                        load(ppp[1].value[0]+".lv")
                        lvhistory.append(ppp[1].value[0])
            if event.key==pygame.K_r:
                load(lvhistory[-1]+".lv")
            if event.key==pygame.K_ESCAPE and len(lvhistory)>1:
                lvhistory.pop(-1)
                load(lvhistory[-1]+".lv")
    w.fill((0, 0, 0))
    fit=min(w.get_width(), w.get_height())*0.8
    drawlevel(lvvll.id, (w.get_width()-fit)/2, (w.get_height()-fit)/2, fit)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()