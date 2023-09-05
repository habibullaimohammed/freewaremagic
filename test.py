from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.middleware("http")
async def remove_whitespace_middleware(request: Request, call_next):
    # Get the original URL
    original_url = request.url

    # Remove %20 and whitespace from the URL
    cleaned_url = original_url.replace("%20", "").replace(" ", "")

    # Create a new Request object with the cleaned URL
    cleaned_request = request.copy()
    cleaned_request.url = cleaned_url

    # Call the next middleware or handler with the cleaned request
    response = await call_next(cleaned_request)

    return response

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
