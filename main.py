
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# ---------------------------
# Root Route (health check)
# ---------------------------
@app.get("/")
async def root():
    return {"status": "running"}


# ---------------------------
# GET Handshake (required by eBay)
# ---------------------------
@app.get("/ebay/notifications/deletion")
async def ebay_deletion_get(challenge_code: str = None):
    """
    eBay calls this first using GET:
    /ebay/notifications/deletion?challenge_code=<token>
    """
    if challenge_code:
        return {"challengeResponse": challenge_code}

    return {"message": "missing challenge_code"}


# ---------------------------
# POST Notification Handler
# ---------------------------

VERIFICATION_TOKEN = "12345678901234567890123456789012"

class EbayDeletionNotification(BaseModel):
    challengeCode: str | None = None
    verificationToken: str | None = None
    # eBay may send additional fields — we accept them using **kwargs in the route


@app.post("/ebay/notifications/deletion")
async def ebay_deletion_post(request: Request):
    """
    Handles eBay's POST validation + real deletion notifications.
    """
    data = await request.json()

    # 1. POST validation (eBay sends challengeCode)
    if "challengeCode" in data:
        return {
            "challengeResponse": data["challengeCode"],
            "verificationToken": VERIFICATION_TOKEN
        }

    # 2. Log actual deletion notification (for later use)
    print("Received eBay deletion message:", data)

    # 3. Always return 200 OK acknowledgment
    return {"ack": "true"}
