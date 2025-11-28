
from fastapi import FastAPI, Request
from pydantic import BaseModel
import hashlib

app = FastAPI()

# ==== eBay config (KEEP THESE IN SYNC WITH EBAY SETTINGS) ====
VERIFICATION_TOKEN = "12345678901234567890123456789012"
ENDPOINT_URL = "https://ebay-deletion-endpoint-z0i3.onrender.com/ebay/notifications/deletion"
# =============================================================


# ---------------------------
# Root route (health check)
# ---------------------------
@app.get("/")
async def root():
    return {"status": "running"}


# ---------------------------
# eBay Deletion Notification
# ---------------------------

class EbayDeletionNotification(BaseModel):
    challengeCode: str | None = None
    # eBay may send additional fields (userId, reason, etc.)
    # We'll just accept the raw body for now.


# 1) VALIDATION: eBay sends a GET with ?challenge_code=...
@app.get("/ebay/notifications/deletion")
async def ebay_deletion_validation(challenge_code: str | None = None):
    if challenge_code:
        # Build the string exactly as eBay expects:
        # challengeCode + verificationToken + endpointUrl
        combined = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL

        # SHA-256 hash -> hex string
        response_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()

        # Debug logging (shows up in Render logs)
        print("eBay validation request")
        print("challenge_code:", challenge_code)
        print("response_hash:", response_hash)

        # FastAPI will send this as application/json
        return {"challengeResponse": response_hash}

    # If someone hits the URL without a challenge_code
    return {"status": "ok"}


# 2) ACTUAL NOTIFICATIONS: eBay sends a POST with JSON body
@app.post("/ebay/notifications/deletion")
async def ebay_deletion_handler(request: Request):
    data = await request.json()
    print("Received eBay deletion message:", data)

    # For now we just acknowledge; later you can add your own logic
    return {"ack": "true"}
