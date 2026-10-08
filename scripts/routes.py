from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
import json, urllib.request, time
P = {
 "polo": (36.10653,-115.17085), "vof": (36.42999,-114.51377), "kanab": (37.04692,-112.52590),
 "imperial": (36.27832,-111.97767), "royal": (36.12246,-111.94998), "nrvc": (36.19840,-112.05230),
 "dunes": (37.04059,-112.71315), "fourc": (36.99864,-109.04468), "kayenta": (36.70766,-110.25391),
 "view": (36.98212,-110.11185), "antelope": (36.86257,-111.37469), "waldorf": (36.10621,-115.17436),
}
SEG = [
 (1,"Las Vegas → Valley of Fire → Kanab",["polo","vof","kanab"]),
 (2,"Kanab → North Rim (Cape Royal, Point Imperial, Visitor Center) → Kanab",["kanab","royal","imperial","nrvc","kanab"]),
 (2,"Kanab → Coral Pink Sand Dunes (sunset) → Kanab",["kanab","dunes","kanab"]),
 (3,"Kanab → Four Corners Monument → Kayenta",["kanab","fourc","kayenta"]),
 (3,"Kayenta → The View, Monument Valley (stargazing) → Kayenta",["kayenta","view","kayenta"]),
 (4,"Kayenta → Upper Antelope Canyon (Page) → Las Vegas",["kayenta","antelope","waldorf"]),
]
def dp(pts, eps):
    if len(pts)<3: return pts
    import math
    (x1,y1),(x2,y2)=pts[0],pts[-1]
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1e-12
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        x,y=pts[i]; d=abs(dy*x-dx*y+x2*y1-y2*x1)/L
        if d>dmax: dmax,idx=d,i
    if dmax>eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [pts[0],pts[-1]]
out=[]
for day,name,stops in SEG:
    coords=";".join(f"{P[s][1]},{P[s][0]}" for s in stops)
    url=f"https://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson&steps=true"
    r=json.load(urllib.request.urlopen(url))["routes"][0]
    line=[(round(lat,5),round(lon,5)) for lon,lat in r["geometry"]["coordinates"]]
    k=max(range(len(line)),key=lambda i:(line[i][0]-line[0][0])**2+(line[i][1]-line[0][1])**2)
    simp=dp(line[:k+1],0.00015)[:-1]+dp(line[k:],0.00015)
    roads=[]
    for leg in r["legs"]:
        for st in leg["steps"]:
            n=st.get("ref") or st.get("name")
            if n and st["distance"]>8000 and n not in roads: roads.append(n)
    out.append(dict(day=day,name=name,stops=stops,miles=round(r["distance"]/1609.34,1),hours=round(r["duration"]/3600,2),
        legs=[dict(mi=round(l["distance"]/1609.34,1),h=round(l["duration"]/3600,2)) for l in r["legs"]],line=simp,roads=roads))
    print(day,out[-1]["miles"],"mi",out[-1]["hours"],"h",len(line),"->",len(simp),roads)
    time.sleep(1)
json.dump(dict(points=P,segments=out),open(ROOT/"data/trip.json","w"),separators=(",",":"))
