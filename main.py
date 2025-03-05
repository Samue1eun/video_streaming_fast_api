import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from dotenv import load_dotenv
from supabase import create_client, Client
import httpx
from datetime import datetime, UTC

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates

templates = Jinja2Templates(directory="templates")

templates.env.globals.update(now=lambda: datetime.now(UTC))

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    videos = supabase.storage.from_(SUPABASE_BUCKET).list()
    return templates.TemplateResponse('home.html', {'request': request, 'videos': videos})