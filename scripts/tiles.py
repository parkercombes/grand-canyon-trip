from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
import json,math,os,base64,urllib.request,concurrent.futures as cf
d=json.load(open(ROOT/"data/trip.json"))
def t(lat,lon,z):
    n=2**z; x=int((lon+180)/360*n); y=int((1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n); return x,y
pts=[p for s in d["segments"] for p in s["line"]]
lats=[p[0] for p in pts]; lons=[p[1] for p in pts]
need={}
for z in range(5,13):
    s=set()
    if z<=10:
        p=1.6 if z<=9 else .9; x0,y0=t(max(lats)+p,min(lons)-p,z); x1,y1=t(min(lats)-p,max(lons)+p,z)
        s={(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)}
    else:
        for la,lo in pts:
            x,y=t(la,lo,z)
            s|={(x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1)}
    need[z]=s
os.makedirs(ROOT/".tile-cache",exist_ok=True)
def get(job):
    svc,z,x,y=job
    fn=f"{ROOT}/.tile-cache/{svc}_{z}_{x}_{y}.jpg"
    if os.path.exists(fn) and os.path.getsize(fn)>0: return
    for _ in range(3):
        try:
            data=urllib.request.urlopen(urllib.request.Request(f"https://basemap.nationalmap.gov/arcgis/rest/services/{svc}/MapServer/tile/{z}/{y}/{x}",headers={"User-Agent":"personal-trip-map/1.0"}),timeout=30).read()
            open(fn,"wb").write(data); return
        except Exception as e: err=e
    print("fail",job,err)
jobs=[(svc,z,x,y) for svc in ("USGSTopo","USGSImageryTopo") for z in need for (x,y) in need[z]]
print(len(jobs),"tiles")
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(get,jobs))
os.makedirs(ROOT/"tiles",exist_ok=True)
groups={"lo":range(5,9),"z9":[9],"z10":[10],"z11":[11],"z12":[12]}
for svc,short in (("USGSTopo","topo"),("USGSImageryTopo","sat")):
    for g,zs in groups.items():
        b={}
        for z in zs:
            for x,y in need[z]:
                fn=f"{ROOT}/.tile-cache/{svc}_{z}_{x}_{y}.jpg"
                if os.path.exists(fn) and os.path.getsize(fn)>0: b[f"{z}/{x}/{y}"]=base64.b64encode(open(fn,"rb").read()).decode()
        json.dump(b,open(f"{ROOT}/tiles/{short}_{g}.json","w"))
        print(short,g,len(b),os.path.getsize(f"{ROOT}/tiles/{short}_{g}.json")//1024,"KB")
