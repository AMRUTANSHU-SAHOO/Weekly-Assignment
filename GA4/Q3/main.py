from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
async def get_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.HTTPStatusError:
        return {"error": f"Could not fetch page for country: {country}"}

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    outline = []
    for tag in headings:
        level = int(tag.name[1])  # Extract the number from h1, h2, etc.
        text = tag.get_text(strip=True)
        outline.append(f"{'#' * level} {text}")

    return "\n".join(outline)