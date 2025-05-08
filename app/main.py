from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .api import auth, career, profile
from .db.csv_storage import init_csv_files

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5200",
        "http://127.0.0.1:5200"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Root route to serve index.html
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard route
@app.get("/dashboard")
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/profile")
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

# Initialize CSV files
@app.on_event("startup")
def init_storage():
    init_csv_files()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(career.router, prefix="/career", tags=["career"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"]) 