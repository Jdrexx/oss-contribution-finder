from __future__ import annotations
import csv, io, re, sqlite3
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
APP_NAME='Open Source Contribution Finder'
DB_FILE=Path(__file__).resolve().parent.parent/'data'/'app.sqlite'
DB_FILE.parent.mkdir(exist_ok=True)
app=FastAPI(title=APP_NAME, version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
def json_dumps(obj: Any) -> str:
    import json; return json.dumps(obj, ensure_ascii=False)
def json_loads(text: str) -> Any:
    import json; return json.loads(text)
def db() -> sqlite3.Connection:
    conn=sqlite3.connect(DB_FILE); conn.row_factory=sqlite3.Row; conn.execute('pragma journal_mode=wal'); return conn
def init_db() -> None:
    with db() as conn: conn.execute('create table if not exists records (id integer primary key autoincrement, kind text not null, title text not null, payload text not null, created_at text not null)')
init_db()
def save_record(kind: str, title: str, payload: str) -> int:
    with db() as conn:
        cur=conn.execute('insert into records(kind,title,payload,created_at) values (?,?,?,?)',(kind,title,payload,datetime.utcnow().isoformat())); return int(cur.lastrowid)
def rows(kind: str | None = None) -> list[dict[str, Any]]:
    with db() as conn:
        data=conn.execute('select * from records where kind=? order by id desc',(kind,)).fetchall() if kind else conn.execute('select * from records order by id desc').fetchall()
    return [dict(r) for r in data]
@app.get('/api/health')
def health(): return {'ok': True, 'app': APP_NAME, 'records': len(rows())}
@app.get('/', response_class=HTMLResponse)
def home(): return INDEX_HTML

from urllib.parse import quote
class SearchRequest(BaseModel):
    skills: str
    language: str = ""
    difficulty: str = "any"
def estimate_difficulty(body: str, title: str) -> str:
    t = (body + " " + title).lower()
    if any(w in t for w in ['easy','good first','beginner','simple']): return 'easy'
    if any(w in t for w in ['hard','complex','advanced']): return 'hard'
    return 'medium'
def estimate_time(difficulty: str) -> str:
    return {'easy':'~1-2h','medium':'~3-6h','hard':'~1-2 days'}.get(difficulty, '~3-6h')
@app.post('/api/search')
def search_issues(req: SearchRequest):
    import urllib.request
    q = quote(req.skills)
    lang = f"+language:{req.language}" if req.language else ""
    url = f"https://api.github.com/search/issues?q={q}{lang}+label:good-first-issue+state:open&sort=updated&per_page=12"
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"oss-finder/0.1","Accept":"application/vnd.github.v3+json"}), timeout=15)
        data = json_loads(resp.read().decode())
        results=[]
        for item in data.get('items',[])[:10]:
            diff = estimate_difficulty(item.get('body',''), item.get('title',''))
            if req.difficulty != 'any' and diff != req.difficulty: continue
            results.append({"title": item['title'], "repo": item['repository_url'].split('/')[-1], "url": item['html_url'], "difficulty": diff, "estimate": estimate_time(diff), "created": item.get('created_at','')[:10], "score": item.get('score',0)})
        save_record('search', req.skills, json_dumps({"query": req.skills, "results": results}))
        return {"count": len(results), "results": results}
    except Exception as e:
        return {"count": 0, "results": [], "error": str(e), "note": "GitHub API call failed; try again later."}
@app.get('/api/bookmarks')
def bookmarks():
    return {"bookmarks": [json_loads(r['payload']) | {'id':r['id'],'created_at':r['created_at']} for r in rows('search')]}

INDEX_HTML='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Source Contribution Finder</title><style>body{font-family:Inter,Arial,sans-serif;background:#0f172a;color:#e5e7eb;margin:0}main{max-width:980px;margin:auto;padding:32px}.card{background:#111827;border:1px solid #334155;border-radius:18px;padding:24px;margin:18px 0}h1{font-size:42px}textarea,input{width:100%;box-sizing:border-box;border-radius:12px;border:1px solid #475569;background:#020617;color:#e5e7eb;padding:14px;margin:8px 0}button{background:#22c55e;color:#04130a;border:0;border-radius:12px;padding:12px 18px;font-weight:700}pre{white-space:pre-wrap;background:#020617;border-radius:12px;padding:16px}.pill{background:#1e293b;border:1px solid #475569;border-radius:999px;padding:6px 10px}</style></head><body><main><div class="card"><span class="pill">developer productivity</span><h1>Open Source Contribution Finder</h1><p>Search GitHub issues by skill, filter by difficulty, and find your first open-source contribution.</p><ul><li>Search GitHub issues by skill keywords</li><li>Filter by language and difficulty</li><li>Estimated time-to-fix indicator</li><li>Bookmark interesting issues</li><li>GitHub API integration</li></ul></div><div class="card"><h2>Live Demo</h2><textarea id="input" rows="6">React Python FastAPI</textarea><input id="input2" placeholder="language (optional)" value="python" /><button onclick="runDemo()">Run</button><pre id="out">Click Run to call the API.</pre></div><div class="card"><h2>API</h2><p>Health: /api/health &middot; Docs: /docs</p></div><script>async function runDemo(){const res=await (fetch(\'/api/search\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({skills:document.getElementById(\'input\').value,language:document.getElementById(\'input2\').value||\'\',difficulty:\'any\'})}));document.getElementById(\'out\').textContent=JSON.stringify(await res.json(),null,2);}</script></main></body></html>'
