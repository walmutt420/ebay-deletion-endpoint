from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "running"}

# --------------------------
# Required GET validation
# --------------------------
@app.get("/ebay/notifications/deletion")
async def ebay_deletion_get(challenge_code: str = None):
    if challenge_code:
        return {"challengeResponse": challenge_code}
    return {"message": "missing challenge_code"}

# --------------------------
# POST validation + events
# --------------------------
VERIFICATION_TOKEN = "12345678901234567890123456789012"

class EbayDeletionNotification(BaseModel):
    challengeCode: str | None = None
    verificationToken: str | None = None

@app.post("/ebay/notifications/deletion")
async def ebay_deletion_post(request: Request):
    data = await request.json()

    # POST handshake
    if "challengeCode" in data:
        return {
            "challengeResponse": data["challengeCode"],
            "verificationToken": VERIFICATION_TOKEN
        }

    # Actual deletion event
    print("Received eBay deletion message:", data)

    return {"ack": "true"}
