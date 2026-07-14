from fastapi import FastAPI

from api.routes.catalogue_route import router as catalogue_router

app = FastAPI(title="Content Metadata Builder Agent")

app.include_router(catalogue_router)

@app.get("/")
def health_check():
    return {"status" : "server is running"}