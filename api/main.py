from fastapi import FastAPI

# create a default fast api starter template
app = FastAPI()


# TODO make a post request instead of get
@app.get("/")
def read_root():
    return {"Hello": "World"}







