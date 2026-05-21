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
lvname=""
wons={}
progress={}
bgobjs={"win", "lv", "star", "unstar", "oneway", "sign", "levellock"}
lvhistory=[("hub", None), ("w1", (2, 1)), ("w1-1", (2, 2))]
removee=set()
undo=[]
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
class obj:
    def __init__(self, typee, value=None):
        self.type=typee
        self.value=value
def newlevel(dimensions, name, color=(230, 230, 230)):
    lvs[name]=lv(dimensions, name, color)
    return lvs[name]
def drawlevel(name, x, y, scaley, frame=1, playeranim=(0, 0)):
    def star(color, center, outr, inr):
        points=[]
        for i in range(10):
            radius=outr if i%2==0 else inr
            angle=i*(math.pi/5)-(math.pi/2)
            xx=center[0]+radius*math.cos(angle)
            yy=center[1]+radius*math.sin(angle)
            points.append((xx, yy))
        pygame.draw.polygon(w, color, points)
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
    inflock=pygame.image.load("assets/inflock.png").convert_alpha()
    ww, h=inflock.get_size()
    r=tilesizey/h
    inflock=pygame.transform.smoothscale(inflock, (ww*r, h*r))
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
            pygame.draw.circle(w, (0, 0, 0), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex*0.425, width=int(tilesizex*0.175))
            pygame.draw.circle(w, (255, 255, 255) if typee.value[0] not in wons else (255, 255, 0), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex*0.4, width=int(tilesizex*0.1))
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
        elif typee.type=="oneway":
            beltrect=pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey))
            pygame.draw.rect(w, (120, 70, 20), beltrect)
            pygame.draw.rect(w, (210, 160, 10), beltrect, width=int(tilesizex*0.1))
            dxx=x+tilesizex*(pos[0]+0.5)
            dyy=y+tilesizey*(pos[1]+0.5)
            dx, dy=typee.value
            dx=-dx
            dy=-dy
            start=(dxx-(-dx*tilesizex*0.3), dyy+dy*tilesizey*0.3)
            start2=(dxx-(-dy*tilesizex*0.3), dyy-dx*tilesizey*0.3)
            start3=(dxx-(+dy*tilesizex*0.3), dyy+dx*tilesizey*0.3)
            end=(dxx-(dx*tilesizex*0.3), dyy-dy*tilesizey*0.3)
            pygame.draw.line(w, (255, 230, 100), start, end, width=int(tilesizex*0.15))
            pygame.draw.line(w, (255, 230, 100), start2, end, width=int(tilesizex*0.15))
            pygame.draw.line(w, (255, 230, 100), start3, end, width=int(tilesizex*0.15))
        elif typee.type=="star":
            star((255, 255, 255), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex/3+tilesizex/10, tilesizex/6+tilesizex/15)
            star((255, 234, 8), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex/3, tilesizex/6)
        elif typee.type=="unstar":
            star((255, 255, 255), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex/3+tilesizex/10, tilesizex/6+tilesizex/15)
            star((255, 0, 0), (x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5)), tilesizex/3, tilesizex/6)
        elif typee.type=="levellock":
            cc=checklvlock(typee)
            pygame.draw.rect(w, (max(0, min(255, int(lvs[name].color[0]*0.4+80))), max(0, min(255, int(lvs[name].color[1]*0.4))), max(0, min(255, int(lvs[name].color[2]*0.4)))) if not cc[1] else (max(0, min(255, int(lvs[name].color[0]*0.4))), max(0, min(255, int(lvs[name].color[1]*0.4))), max(0, min(255, int(lvs[name].color[2]*0.4)))), pygame.Rect(math.floor(x+tilesizex*pos[0]), math.floor(y+tilesizey*pos[1]), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2))
            surf=font3.render(str(cc[0])+"/"+typee.value, False, (0, 0, 0))
            npos=(x+tilesizex*(pos[0]+0.5), y+tilesizey*(pos[1]+0.5))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
    for pos, (id, typee) in lvs[name].obj.items():
        rrx=x+tilesizex*pos[0]
        rry=y+tilesizey*pos[1]
        if id in animation and frame < 1:
            atypee, dxy=animation[id]
            if atypee=="push":
                rrx-=dxy[0]*tilesizex*(1-frame)
                rry-=dxy[1]*tilesizey*(1-frame)
        if typee.type=="wall":
            pygame.draw.rect(w, (min(int(lvs[name].color[0]*1.4), 255), min(int(lvs[name].color[1]*1.4), 255), min(int(lvs[name].color[2]*1.4), 255)), pygame.Rect(math.floor(rrx), math.floor(rry), math.ceil(tilesizex), math.ceil(tilesizey)))
        elif typee.type=="lock":
            pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(rrx), math.floor(rry), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2))
            if typee.value in {"Err.", "??"}:
                surf=font3.render(typee.value, False, (0, 0, 0))
            else:
                surf=font.render(typee.value, False, (0, 0, 0))
            npos=(rrx+tilesizex*0.5, rry+tilesizey*0.5)
            npos=(rrx+tilesizex*0.5, rry+tilesizey*0.5)
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
        elif typee.type=="key":
            if typee.value in {"Err.", "??"}:
                surf=font3.render(typee.value, False, (255, 255, 255))
                surf2=font3.render(typee.value, False, (0, 0, 0))
            else:
                surf=font.render(typee.value, False, (255, 255, 255))
                surf2=font.render(typee.value, False, (0, 0, 0))
            npos=(rrx+tilesizex*0.5, rry+tilesizey*0.5)
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2+tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2-tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2+tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2-tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2+tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2+tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2-tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2-tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2-tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2+tilesizey/30))
            w.blit(surf2, surf2.get_rect(center=npos).move(-surf2.get_bounding_rect().center[0]+surf2.get_width()/2+tilesizex/30, -surf2.get_bounding_rect().center[1]+surf2.get_height()/2-tilesizey/30))
            w.blit(surf, surf.get_rect(center=npos).move(-surf.get_bounding_rect().center[0]+surf.get_width()/2, -surf.get_bounding_rect().center[1]+surf.get_height()/2))
        elif typee.type=="inflock":
            w.blit(inflock, inflock.get_rect(center=(rrx+tilesizex*0.5, rry+tilesizey*0.5)))
    rrrx=x+tilesizex*(player[0]-playeranim[0]*(1-frame))
    rrry=y+tilesizey*(player[1]-playeranim[1]*(1-frame))
    pygame.draw.rect(w,(0, 0, 0), pygame.Rect(math.floor(rrrx-tilesizex*0.025), math.floor(rrry-tilesizey*0.025), math.ceil(tilesizex+tilesizex*0.025), math.ceil(tilesizey+tilesizey*0.025)), border_radius=int(tilesizex*0.2), width=int(tilesizex*0.175))
    pygame.draw.rect(w, (255, 255, 255), pygame.Rect(math.floor(rrrx), math.floor(rrry), math.ceil(tilesizex), math.ceil(tilesizey)), border_radius=int(tilesizex*0.2), width=int(tilesizex*0.1))
def push(id, dxy, max_depth=99, typpe=None):
    if id==-1: return True
    if max_depth<1: return False
    dx=dxy[0]
    dy=dxy[1]
    lvv=lvs[objlvs[id]]
    typeee=lvv.obj2[id][1]
    if typeee.type=="wall": return False
    pos, typeeee=lvv.obj2[id]
    bgg=lvv.bg.get(pos, (-1, None))
    if bgg[1] is not None and bgg[1].type=="oneway" and bgg[1].value==(-dx, -dy): return False
    if typpe is None: typpe=typeeee
    newpos=(pos[0]+dx, pos[1]+dy)
    bgg=lvv.bg.get(newpos, (-1, None))
    if bgg[1] is not None and bgg[1].type=="oneway" and bgg[1].value==(-dx, -dy): return False
    (nid, typee)=lvv.obj.get(newpos, (-1, None))
    if newpos[0]<0 or newpos[0]>=lvv.dimensions[0] or newpos[1]<0 or newpos[1]>=lvv.dimensions[1]: return False
    if typee!=None and typee.type!=typpe.type: return False
    pushh=nid==-1
    if not pushh: pushh=push(nid, dxy, max_depth=max_depth-1, typpe=typpe)
    if pushh:
        lvv.teleport(id, newpos)
        modified[pos]=True
        modified[newpos]=True
        animation[nid]=("push", dxy)
        animation[id]=("push", dxy)
        return True
    return False
def calculatestr(expr):
    def evalop(l, op, r):
        if l=="Err." or r=="Err.": return "Err."
        if l=="??" or r=="??": return "??"
        if l=="?" or r=="?":
            if op=="*":
                if l=="0" or r=="0": return "0"
                return "?"
            if op=="/":
                if r=="0": return "??"
                if l=="?":
                    if r=="?": return "??"
                    return "?"
                if l=="0": return "?"
                return "??"
            return "?"
        l=int(l)
        r=int(r)
        if op=="+": return str(l+r)
        if op=="-": return str(l-r)
        if op=="*": return str(l*r)
        if op=="/":
            if r==0:
                if l==0:
                    return "?"
                return "Err."
            if l%r!=0: return ValueError
            return str(l//r)
    i=0
    read=""
    opp=""
    ll=""
    rr=""
    numstart=False
    signs=set("+-")
    numbers=set("0123456789?Er.")
    if expr[-1] not in numbers: raise ValueError
    while i<len(expr):
        if expr[i] in numbers:
            read+=expr[i]
            numstart=True
        elif expr[i] in signs and not numstart:
            read+=expr[i]
        else:
            if read=="": raise ValueError
            else:
                if opp=="":
                    ll=read
                else:
                    rr=read
                    ll=evalop(ll, opp, rr)
                if i==len(expr)-1: return ll
                opp=expr[i]
                read=""
                numstart=False
        i+=1
    if opp=="":
        ll=read
    else:
        rr=read
        ll=evalop(ll, opp, rr)
    if i==len(expr)-1: return ll
    return ll
def checkeq(lvv):
    global player
    symbols={"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "?", "??", "Err."}
    ops=set("+-*/")
    ll=list(lvv.obj.keys())
    for pos in ll:
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
                ans=str(calculatestr(eq))
                sat=True
                if ans=="Err." or ans=="??":
                    neepos=(x+1, y)
                    if neepos in lvv.obj or neepos[0]>=lvv.dimensions[0]:
                        sat=False
                        break
                else:
                    for i in range(len(ans)):
                        neepos=(x+i+1, y)
                        if neepos in lvv.obj or neepos[0]>=lvv.dimensions[0]:
                            sat=False
                            break
                if sat:
                    for eid in iddd:
                        poss=lvv.obj2[eid][0]
                        bg=lvv.bg.get(poss, (-1, None))
                        if (poss!=player and (bg[0]==-1 or bg[1].type!="star")) or (bg[0]!=-1 and bg[1].type=="unstar"): removee.add(eid)
                    bg=lvv.bg.get(pos, (-1, None))
                    if (pos!=player and (bg[0]==-1 or bg[1].type!="star")) or (bg[0]!=-1 and bg[1].type=="unstar"): removee.add(idd)
                    if ans=="Err." or ans=="??":
                        newpos=(x+1, y)
                        nid=lvv.add(obj(typee.type, ans), newpos)
                        animation[nid]=("push", (1, 0))
                    else:
                        for i, char in enumerate(ans):
                            newpos=(x+i+1, y)
                            nid=lvv.add(obj(typee.type, char), newpos)
                            animation[nid]=("push", (1, 0))
            except Exception:
                continue
    for pos in ll:
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
                ans=str(calculatestr(eq))
                sat=True
                if ans=="Err." or ans=="??":
                    neepos=(x, y+1)
                    if neepos in lvv.obj or neepos[1]>=lvv.dimensions[1]:
                        sat=False
                        break
                else:
                    for i in range(len(ans)):
                        neepos=(x, y+i+1)
                        if neepos in lvv.obj or neepos[1]>=lvv.dimensions[1]:
                            sat=False
                            break
                if sat:
                    for eid in iddd:
                        poss=lvv.obj2[eid][0]
                        bg=lvv.bg.get(poss, (-1, None))
                        if (poss!=player and (bg[0]==-1 or bg[1].type!="star")) or (bg[0]!=-1 and bg[1].type=="unstar"): removee.add(eid)
                    bg=lvv.bg.get(pos, (-1, None))
                    if (pos!=player and (bg[0]==-1 or bg[1].type!="star")) or (bg[0]!=-1 and bg[1].type=="unstar"): removee.add(idd)
                    if ans=="Err." or ans=="??":
                        newpos=(x, y+1)
                        nid=lvv.add(obj(typee.type, ans), newpos)
                        animation[nid]=("push", (0, 1))
                    else:
                        for i, char in enumerate(ans):
                            newpos=(x, y+i+1)
                            nid=lvv.add(obj(typee.type, char), newpos)
                            animation[nid]=("push", (0, 1))
            except Exception:
                continue
def cancel(lvv):
    for pos, (idd, typee) in list(lvv.obj.items()):
        if typee.type=="lock":
            x, y=pos
            next=[(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            for newpos in next:
                if newpos in lvv.obj:
                    nid, typeee=lvv.obj[newpos]
                    if typeee.type=="key" and (typeee.value==typee.value or typeee.value=="??" or typee.value=="??"):
                        if idd!=player: removee.add(idd)
                        if nid!=player: removee.add(nid)
        elif typee.type=="inflock":
            x, y=pos
            next=[(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            for newpos in next:
                if newpos in lvv.obj:
                    nid, typeee=lvv.obj[newpos]
                    if typeee.type=="key" and typeee.value=="??":
                        removee.add(idd)
                        if nid!=player: removee.add(nid)
    for iidd in removee:
        lvv.remove(iidd)
def win(lvv):
    global animation, move
    for pos, (idd, typee) in list(lvv.bg.items()):
        if typee.type=="win":
            if player==pos:
                wons[lvhistory[-1][0]]=True
                if len(lvhistory)>1:
                    lvhistory.pop(-1)
                    load("assets/"+lvhistory[-1][0]+".lv")
                    animation={}
                    move=(0, 0)
                    saveprogress("assets/progress.prg")


def checklvlock(obj):
    completed=0
    for pos, (id, typee) in lvvll.bg.items():
        if typee.type=="lv":
            if typee.value[0] in wons:
                completed+=1
    return completed, completed>=int(obj.value)
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
    global lvvll, objlvs, next_free, player, lvname
    with open(file, "rb") as f: load=pickle.load(f)
    lvname=file[7:-3] #will change to be stored on seperate file soon because i do NOT want to remake all of my hub levels to change the names
    lvvll=load["level"]
    objlvs=load["objlvs"]
    next_free=load["next_free"]
    player=load["player"]
    lvs[lvvll.id]=lvvll
def saveprogress(save):
    global progress
    progress=wons.copy()
    with open(save, "wb") as f: pickle.dump(progress, f)
def loadprogress(save):
    global wons
    with open(save, "rb") as f: progress=pickle.load(f)
    wons=progress.copy()
def clearprogress(save):
    global progress, wons
    progress={}
    wons={}
    with open(save, "wb") as f: pickle.dump(progress, f)
def createlv():
    global player, lvvll;
    lvvll=newlevel((18, 15), "root", color=(0, 0, 0));
    lvvll.add(obj("wall"), (0, 14));
    lvvll.add(obj("wall"), (17, 1));
    lvvll.add(obj("wall"), (17, 0));
    player=(7, 2)
#createlv(); save("assets/2.lv")
load("assets/w1-1.lv")
#load("assets/w1.lv")
#saveprogress("assets/progress.prg")
loadprogress("assets/progress.prg")
#clearprogress("assets/progress.prg")
clock=pygame.time.Clock()
x=True
while x:
    move=None
    for event in pygame.event.get():
        if event.type==pygame.QUIT: x=False
        elif event.type==pygame.KEYDOWN:
            modified={}
            animation={}
            move=None
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE, pygame.K_r, pygame.K_ESCAPE): undo.append(pickle.dumps({"level": lvvll, "objlvs": objlvs, "next_free": next_free, "player": player, "lvhistory": lvhistory}))
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
                    sc=push(pp[0], move)
                    try:
                        player=lvvll.obj2[pp[0]][0]
                        if not sc: move=(0, 0)
                    except KeyError:
                        player=(player[0]+move[0], player[1]+move[1])
                    removee=set()
                    checkeq(lvvll)
                    cancel(lvvll)
                    try:
                        player=lvvll.obj2[pp[0]][0]
                        win(lvvll)
                    except KeyError:
                        pass
                else:
                    bgg=lvvll.bg.get(player, (-1, None))
                    if not(bgg[1] is not None and bgg[1].type=="oneway" and bgg[1].value==(-move[0], -move[1])):
                        player=(player[0]+move[0], player[1]+move[1])
                        pp=lvvll.obj.get(player, (-1, None))
                        bgg=lvvll.bg.get(player, (-1, None))
                        if (pp[0]!=-1 and pp[1].type in {"wall", "inflock"}) or (bgg[1] is not None and bgg[1].type=="oneway" and bgg[1].value==(-move[0], -move[1])):
                            player=(player[0]-move[0], player[1]-move[1])
                            move=(0, 0)
            ppp=lvvll.bg.get(player, (-1, None))
            if ppp[0]!=-1:
                if ppp[1].type=="lv":
                    if event.key==pygame.K_SPACE:
                        lvhistory.append((ppp[1].value[0], player))
                        load("assets/"+ppp[1].value[0]+".lv")
                elif ppp[1].type=="levellock":
                    if not checklvlock(ppp[1])[1]:
                        load("assets/"+lvhistory[-1][0]+".lv")
                        animation={}
                        move=(0, 0)
            if event.key==pygame.K_r:
                load("assets/"+lvhistory[-1][0]+".lv")
            if event.key==pygame.K_ESCAPE and len(lvhistory)>1:
                load("assets/"+lvhistory[-2][0]+".lv")
                player=lvhistory[-1][1]
                lvhistory.pop(-1)
            if event.key==pygame.K_z:
                if len(undo)>0:
                    last=pickle.loads(undo.pop())
                    lvvll=last["level"]
                    objlvs=last["objlvs"]
                    next_free=last["next_free"]
                    player=last["player"]
                    lvhistory=last["lvhistory"]
                    lvs[lvvll.id]=lvvll
                    move=None
                    animation={}
    w.fill((0, 0, 0))
    fit=min(w.get_width(), w.get_height())*0.8
    if move is None: drawlevel(lvvll.id, (w.get_width()-fit)/2, (w.get_height()-fit)/2, fit)
    else:
        for i in range(-4, 4):
            drawlevel(lvvll.id, (w.get_width()-fit)/2, (w.get_height()-fit)/2, fit, frame=(math.cbrt(i/4)+1)/2, playeranim=move)
            pygame.display.flip()
            clock.tick(60)
            w.fill((0, 0, 0))
        drawlevel(lvvll.id, (w.get_width()-fit)/2, (w.get_height()-fit)/2, fit, frame=1)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()