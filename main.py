from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "running"}


# ---------------------------
# GET Handshake (required by eBay)
# ---------------------------

@app.get("/ebay/notifications/deletion")
async def ebay_deletion_get(challenge_code: str = None):
    if challenge_code:
        return {"challengeResponse": challenge_code}
    return {"message": "missing challenge_code"}


# ---------------------------
# POST Notification Handler
# ---------------------------

class EbayDeletionNotification(BaseModel):
    challengeCode: str | None = None
    verificationToken: str | None = None

@app.post("/ebay/notifications/deletion")
async def ebay_deletion_post(data: EbayDeletionNotification):
    # 1. If POST contains a challengeCode, respond
    if data.challengeCode:
        return {
            "challengeResponse": data.challengeCode,
            "verificationToken": data.verificationToken
        }

    print("Received eBay deletion message:", data.dict())
    return {"ack": "true"}
