V=[0,100,320,330,500,900,0];N=[-33,-31,-18,-14,14,18,31,33]
W=[-17,-16,-15,-1,1,15,16,17];B=[-17,-15,15,17];R=[-16,-1,1,16]
ST='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'
CM={0:13,4:12,7:14,112:7,116:3,119:11};I=10**9;NC=16000;nd=[0,0]
def F(f):
 p=f.split();b=[0]*128;r=7;c=0
 for ch in p[0]:
  if ch=='/':r-=1;c=0
  elif ch.isdigit():c+=int(ch)
  else:b[r*16+c]=("PNBRQK".index(ch.upper())+1)*(1-(ch>'Z')*2);c+=1
 k=sum(1<<"KQkq".find(ch)for ch in p[2]if ch in"KQkq")
 e=(int(p[3][1])-1)*16+ord(p[3][0])-97 if p[3]!='-'else-1
 return[b,(p[1]=='w')*2-1,k,e,[]]
def A(b,s,x):
 for ds,pv in(((-15*x,-17*x),1),(N,2),(W,6)):
  for d in ds:
   y=s+d
   if not y&0x88 and b[y]==pv*x:return 1
 for d in W:
  y=s+d
  while not y&0x88:
   v=b[y]
   if v:
    if v in(5*x,(3 if d in B else 4)*x):return 1
    break
   y+=d
 return 0
def M(P,co=0):
 b=P[0];t=P[1];ms=[];ap=ms.append
 for s,v in enumerate(b):
  if v*t<=0:continue
  a=abs(v)
  if a==1:
   d=16*t
   for y in(s+d,s+d-1,s+d+1):
    if y&0x88:continue
    z=y==s+d
    if z and b[y]:continue
    if not z and not(b[y]*t<0 or y==P[3]):continue
    if y>>4 in(0,7):
     for q in(5,4,3,2):ap(s|y<<7|q<<14)
    elif not z or not co:
     ap(s|y<<7)
     if z and(s>>4)==(1 if t>0 else 6)and not b[s+2*d]:ap(s|(s+2*d)<<7)
  else:
   for d in(N if a==2 else B if a==3 else R if a==4 else W):
    y=s+d
    while not y&0x88:
     q=b[y]
     if q*t<0 or(not q and not co):ap(s|y<<7)
     if q:break
     if a in(2,6):break
     y+=d
   if a==6 and not co and s==(4 if t==1 else 116)and not A(b,s,-t):
    for sg,bt in((1,1 if t==1 else 4),(-1,2 if t==1 else 8)):
     if P[2]&bt and b[s+(3 if sg>0 else 4)*sg]==4*t and not(b[s+sg]or b[s+2*sg]or(sg<0 and b[s-3])or A(b,s+sg,-t)or A(b,s+2*sg,-t)):ap(s|(s+2*sg)<<7)
 return ms
def D(P,m):
 b=P[0];f=m&127;y=(m>>7)&127;q=(m>>14)&7;v=b[f];cp=b[y];cs=y
 if abs(v)==1 and y==P[3]and not cp and f&7!=y&7:cs=y-16*P[1];cp=b[cs]
 P[4].append((b,P[2],P[3]));c=b[:];c[f]=0;c[cs]=0;c[y]=q*P[1]if q else v
 if abs(v)==6 and abs(y-f)==2:
  rf=(f&112)+(7 if y>f else 0);c[(f+y)//2]=c[rf];c[rf]=0
 P[0]=c;P[2]&=CM.get(f,15)&CM.get(y,15);P[3]=f+16*P[1]if abs(v)==1 and abs(y-f)==32 else-1;P[1]=-P[1]
def U(P):
 P[0],P[2],P[3]=P[4].pop();P[1]=-P[1]
def L(P,co=0):
 r=[]
 for m in M(P,co):
  D(P,m)
  if not A(P[0],P[0].index(-6*P[1]),P[1]):r.append(m)
  U(P)
 return r
def E(P):
 b=P[0];s=0;c=[0,0]
 for i,v in enumerate(b):
  if v:
   a=abs(v);r=i>>4;c[v>0]+=a==3
   w=V[a]+(10*(r if v>0 else 7-r)if a==1 else(14-abs(7-2*(i&7))-abs(7-2*r))*(4 if a==2 else 1)//2 if 1<a<6 else 0)
   s+=w if v>0 else-w
 s+=25*((c[1]>1)-(c[0]>1))
 return s*P[1]
def O(P,ms):
 b=P[0]
 def k(m):
  y=(m>>7)&127;q=(m>>14)&7;vc=abs(b[y])or y==P[3]
  return(9000+V[q]if q else 0)+(10000+V[vc]*16-abs(b[m&127])if vc else 0)
 return sorted(ms,key=k)[::-1]
def S(P,d,a,be,pl):
 nd[0]+=1
 if nd[1]or nd[0]>NC:nd[1]=1;return 0
 if d<=0:
  a=max(a,E(P))
  if a>=be:return be
 ms=L(P,1 if d<=0 else 0)
 if not ms:
  if d>0:return-100000+pl if A(P[0],P[0].index(6*P[1]),-P[1])else 0
  return a
 bs=a if d<=0 else-I
 for m in O(P,ms):
  D(P,m);sc=-S(P,d-1,-be,-a,pl+1);U(P)
  if nd[1]:return 0
  bs=max(bs,sc);a=max(a,sc)
  if a>=be:break
 return bs
def Z(P):
 ms=L(P)
 if not ms:return None
 if len(ms)==1:return ms[0]
 nd[0]=0;nd[1]=0;bs=ms[0];d=0
 while d<5:
  d+=1;a=-I;cur=bs
  for m in O(P,ms):
   D(P,m);sc=-S(P,d-1,-I,-a,1);U(P)
   if nd[1]:break
   if sc>a:a=sc;cur=m
  else:bs=cur
  if nd[1]:break
 return bs
def mu(m):
 def n(s):return chr(97+s%8)+chr(49+s//16)
 q=(m>>14)&7;return n(m&127)+n((m>>7)&127)+('nbrq'[q-2]if q else'')
def choose_move(board,history=None,time_left=None,color=None):
 P=F(board)if board else F(ST)
 m=Z(P);return mu(m)if m is not None else''
def env():
 import json,os,urllib.request as ur
 u=os.environ['MAKEFUN_ENV_URL']
 post=lambda p,pl:json.load(ur.urlopen(u+p,json.dumps(pl).encode()))
 g=post('/game',{})
 while g.get('status')!='done':g=post('/move',{'game':g['game'],'move':choose_move(g['fen'])})
if __name__=='__main__':env()
