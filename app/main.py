from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import init_db
from .routers import dashboard, http_events, pcap, cowrie

app = FastAPI(title="URL Attack Detector MVP")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to ["http://localhost:3000"] when React UI runs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static + Templates ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")

# --- Init DB ---
init_db()

# --- Routers ---
app.include_router(dashboard.router)
app.include_router(http_events.router)
app.include_router(pcap.router)
app.include_router(cowrie.router)

# --- Health Check ---
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
