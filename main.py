from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Your verification token
VERIFICATION_TOKEN = "12345678901234567890123456789012"


# ------------------------------------------------------
# Root (health check)
# ------------------------------------------------------
@app.get("/")
async def root():
    return {"status": "running"}


# ------------------------------------------------------
# GET — Required for eBay validation
# eBay calls: /ebay/notifications/deletion?challenge_code=XYZ
# ------------------------------------------------------
@app.get("/ebay/notifications/deletion")
async def ebay_validation(challenge_code: str = None):
    # This is REQUIRED — eBay will not accept the endpoint without it
    if challenge_code:
        return {"challengeResponse": challenge_code}

    # For debugging if hit without challenge_code
    return {"status": "waiting-for-ebay-validation"}


# ------------------------------------------------------
# POST — Actual deletion notifications
# ------------------------------------------------------
class EbayDeletionNotification(BaseModel):
    challengeCode: str | None = None  # sometimes included
    verificationToken: str | None = None  # may be included
    # eBay may include additional optional fields via **data


@app.post("/ebay/notifications/deletion")
async def ebay_deletion_handler(request: Request):

    data = await request.json()

    # 1. Handle eBay challenge (POST version — sometimes used)
    if "challengeCode" in data:
        return {"challengeResponse": data["challengeCode"]}

    # 2. If eBay sends the verificationToken, we ignore it (we already validated on GET)
    if "verificationToken" in data:
        print("Received verification token:", data["verificationToken"])

    # 3. Log the received deletion request
    print("Received eBay deletion message:", data)

    return {"ack": "true"}
