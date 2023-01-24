from fastapi import FastAPI
from .routers import users, contact, auth, vote
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(contact.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {"Hello": "World"}