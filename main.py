from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "running"}


@app.post("/ebay/notifications/deletion")
async def ebay_deletion_handler(request: Request):
    data = await request.json()

    # Extract fields eBay may send
    challenge = data.get("challengeCode")
    token = data.get("verificationToken")

    # REQUIRED by eBay: send BOTH back during validation
    if challenge and token:
        return {
            "challengeResponse": challenge,
            "verificationToken": token
        }

    # Normal notifications
    print("Received eBay deletion message:", data)
    return {"ack": "true"}
