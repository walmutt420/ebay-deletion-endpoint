from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# ---------------------------
# Verification Token (32–80 chars)
# ---------------------------
VERIFICATION_TOKEN = "12345678901234567890123456789012"


# ---------------------------
# Root route (health check)
# ---------------------------
@app.get("/")
async def root():
    return {"status": "running"}


# ---------------------------
# eBay Deletion Notification Model
# ---------------------------
class EbayDeletionNotification(BaseModel):
    challengeCode: str | None = None
    verificationToken: str | None = None
    # eBay may send other fields as well (ignored safely)


# ---------------------------
# Deletion Endpoint
# ---------------------------
@app.post("/ebay/notifications/deletion")
async def ebay_deletion_handler(request: Request):

    data = await request.json()

    print("RAW DATA FROM EBAY:", data)

    # 1. Challenge handshake — required for verification
    if "challengeCode" in data:
        return {"challengeResponse": data["challengeCode"]}

    # 2. Verify eBay's token matches our configured token
    if data.get("verificationToken") != VERIFICATION_TOKEN:
        print("Invalid verification token received.")
        return {"error": "invalid verification token"}

    # 3. Process the deletion event
    print("EBAY ACCOUNT DELETION EVENT RECEIVED!")
    print(data)

    # 4. Acknowledge receipt
    return {"ack": "true"}

