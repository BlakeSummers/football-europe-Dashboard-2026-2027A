
import json, os, urllib.request, urllib.parse, datetime, sys
KEY=os.environ.get('API_NINJAS_KEY')
if not KEY:
    raise SystemExit('ERROR: GitHub Actions secret API_NINJAS_KEY no está configurado')
BASE='https://api.api-ninjas.com/v1/'
def get(endpoint,params):
    url=BASE+endpoint+'?'+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={'X-Api-Key':KEY,'User-Agent':'UCL-dashboard/1.0'})
    with urllib.request.urlopen(req,timeout=30) as res:
        return json.loads(res.read().decode('utf-8'))
standings=get('soccerstandings',{'league':'ucl','season':2026})
if not isinstance(standings,list) or len(standings)<30:
    raise SystemExit(f'Validación fallida: tabla inesperada, {len(standings) if isinstance(standings,list) else "no-list"} filas; no sobrescribimos datos.')
# Fetch season matches by offset; free endpoint returns up to 50 per page.
all_matches=[]
for offset in range(0,500,50):
    page=get('soccermatches',{'league':'ucl','season':2026,'offset':offset})
    if not isinstance(page,list): raise SystemExit('Formato de partidos inválido; no actualizar.')
    all_matches.extend(page)
    if len(page)<50: break
# Validate unique match ids and scores only for final matches.
ids=[m.get('game_id') for m in all_matches if m.get('game_id')]
if len(ids)!=len(set(ids)): raise SystemExit('IDs de partidos duplicados: abortando')
for m in all_matches:
    if str(m.get('status','')).lower()=='final':
        if m.get('home_score') is None or m.get('away_score') is None:
            raise SystemExit('Partido final sin marcador; validación aborta')
now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
out={'competition':'UEFA Champions League','season':2026,'seasonLabel':'2026-27','updatedAt':now,'source':'API Ninjas Football API','standings':standings,'matches':all_matches,'notice':'Datos recibidos y validados; el proveedor puede tener retrasos.'}
# ensure season values align
if any(r.get('season') not in (None,2026) for r in standings): raise SystemExit('Temporada de tabla incorrecta')
with open('data.json','w',encoding='utf-8') as f: json.dump(out,f,ensure_ascii=False,indent=2)
print(f'OK: {len(standings)} equipos, {len(all_matches)} partidos. Fecha {now}')
