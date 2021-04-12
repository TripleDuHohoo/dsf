import pygame
from tkinter import *
from urllib.request import urlopen
pygame.init()

def sign(n):return -1 if n<0 else 1
def write(rct):
    sz=min((rct[0][3]*m-10)//len(rct[1]),int(1.5*rct[0][2]*m/max(1,len(max(rct[1],key=lambda x:len(x))))))
    font=pygame.font.SysFont('courier',sz,True)
    Y=rct[0][1]*m+y+(rct[0][3]*m-font.get_height()*len(rct[1]))//2
    for txt in rct[1]:
        txt=font.render(txt,True,(50,50,50))
        X=rct[0][0]*m+x+(rct[0][2]*m-txt.get_width())//2
        a.blit(txt,(X,Y))
        Y+=font.get_height()
def chek(rct,pos):return rct[0]*m+x-10<=pos[0]<=(rct[0]+rct[2])*m+x+10 and rct[1]*m+y-10<=pos[1]<=(rct[1]+rct[3])*m+y+10
def rest():
    global dx,dy,lpos,rpos,c,chsn,w,mvng,I,mx
    dx = dy = 0
    lpos = rpos = c = chsn = w = mvng = I = None
    mx = max(mp | {0: 1}) + 1

W,H=1000,600
a=pygame.display.set_mode((W,H),pygame.RESIZABLE)
m=25
x=y=dx=dy=0
lpos=rpos=c=chsn=w=mvng=I=None
try:
    with open('mp.txt','r')as f:mp=eval(f.read())
except:
    with open('mp.txt','w'):pass
    mp={}
mx=max(mp|{0:1})+1

while True:
    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:exit()
        if event.type==pygame.VIDEORESIZE:W,H=a.get_size()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==4:m=min(100,m+1)
            if event.button==5:m=max(5,m-1)
            if event.button==1:c=event.pos
        if event.type==pygame.MOUSEBUTTONUP:
            if event.button==1 and event.pos==c:
                for i,rct in mp.items():
                    if chek(rct[0],event.pos):
                        if chsn and keys[pygame.K_c]:
                            if i in chsn[2]:chsn[2].discard(i)
                            else:chsn[2].add(i)
                        else:
                            chsn=rct
                            I=i
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_s:
                print('saving...')
                with open('mp.txt', 'w')as f:f.write(str(mp))
                print('saved')
            if event.key==pygame.K_l:
                try:
                    print('loading...')
                    mp=eval(urlopen('https://raw.githubusercontent.com/TripleDuHohoo/Host_GP/main/mindmap.txt').read().decode('utf-8'))
                    print('loaded')
                    rest()
                except:
                    print('load error')
            if event.key==pygame.K_d:
                if I in mp:
                    for rct in mp.values():
                        rct[2].discard(I)
                    mp.pop(I)
                    chsn=None
            if event.key==pygame.K_ESCAPE:chsn=None
            if event.key==pygame.K_w and chsn:
                w=True
                root=Tk()
                root.geometry('500x250')
                input=Text(font='courier 20')
                input.insert(0.0,'\n'.join(chsn[1]))
                input.pack()
                break
    a.fill((225,225,225))
    for i in range(x%m,W,m):pygame.draw.line(a,(150,150,150),(i,0),(i,H))
    for i in range(y%m,H,m):pygame.draw.line(a,(150,150,150),(0,i),(W,i))
    q=pygame.mouse.get_pressed(3)
    pos=pygame.mouse.get_pos()
    if q[0]:
        if mvng:
            dx+=pos[0]-lpos[0]
            dy+=pos[1]-lpos[1]
            chsn[0][0]+=sign(dx)*int(dx//(sign(dx)*m))
            chsn[0][1]+=sign(dy)*int(dy//(sign(dy)*m))
            dx=dx%(sign(dx)*m)
            dy=dy%(sign(dy)*m)
        elif lpos:
            x+=pos[0]-lpos[0]
            y+=pos[1]-lpos[1]
        if chsn and chek(chsn[0],pos):mvng=True
        lpos=pos
    else:
        lpos=mvng=None
        dx=dy=0
    if q[2]:
        if rpos:
            pos=((pos[0]-rpos[0]*m-x)//m+1,(pos[1]-rpos[1]*m-y)//m+1)
            pygame.draw.rect(a,(255,255,255),(m*rpos[0]+x,m*rpos[1]+y,pos[0]*m,pos[1]*m),border_radius=m)
            pygame.draw.rect(a,(50,50,50),(m*rpos[0]+x,m*rpos[1]+y,pos[0]*m,pos[1]*m),3,m)
        else:rpos=[(pos[0]-x)//m,(pos[1]-y)//m]
    else:
        if rpos:
            pos=[(pos[0]-rpos[0]*m-x)//m+1,(pos[1]-rpos[1]*m-y)//m+1]
            if pos[0]<0:
                pos[0]*=-1
                rpos[0]-=pos[0]
            if pos[1]<0:
                pos[1]*=-1
                rpos[1]-=pos[1]
            mp[mx]=[[*rpos,*pos],[''],set()]
            mx+=1
        rpos=None
    for rct in mp.values():
        for con in rct[2]:
            x1,y1=mp[con][0][0]+mp[con][0][2]//2,mp[con][0][1]+mp[con][0][3]//2
            x2,y2=rct[0][0]+rct[0][2]//2,rct[0][1]+rct[0][3]//2
            x3,y3=(x1+x2)//2,(y1+y2)//2
            if abs(x1-x2)>abs(y1-y2):
                pygame.draw.line(a,(0,0,0),(x1*m+x,y1*m+y),(x3*m+x,y1*m+y),3)
                pygame.draw.line(a,(0,0,0),(x3*m+x,y1*m+y),(x3*m+x,y2*m+y),3)
                pygame.draw.line(a,(0,0,0),(x3*m+x,y2*m+y),(x2*m+x,y2*m+y),3)
            else:
                pygame.draw.line(a,(0,0,0),(x1*m+x,y1*m+y),(x1*m+x,y3*m+y),3)
                pygame.draw.line(a,(0,0,0),(x1*m+x,y3*m+y),(x2*m+x,y3*m+y),3)
                pygame.draw.line(a,(0,0,0),(x2*m+x,y3*m+y),(x2*m+x,y2*m+y),3)
    for rct in mp.values():
        pygame.draw.rect(a, (255, 255, 255), (m * rct[0][0] + x,m*rct[0][1]+y,rct[0][2]*m,rct[0][3]*m),border_radius=m)
        pygame.draw.rect(a, (50, 50, 50), (m * rct[0][0] + x, m * rct[0][1] + y, rct[0][2] * m, rct[0][3] * m), 3, m)
        write(rct)
    if chsn:
        pygame.draw.rect(a,(255,150,50),(m*chsn[0][0]+x,m*chsn[0][1]+y,chsn[0][2]*m,chsn[0][3]*m),3,m)
        if w:
            try:
                root.update()
                txt=input.get(0.0,END)
            except:
                txt=txt.split('\n')
                txt.pop()
                chsn[1]=txt
                w=None
    pygame.display.flip()