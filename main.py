from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
import hashlib

app = FastAPI()

# ============================================================
# eBay config – these MUST match what's in the eBay UI
# ============================================================

VERIFICATION_TOKEN = "12345678901234567890123456789012"

# This must match the Marketplace account deletion endpoint field
# exactly, including https:// and the full path.
ENDPOINT_URL = "https://ebay-deletion-endpoint-z0i3.onrender.com/ebay/notifications/deletion"


# ---------------------------
# Root route (health check)
# ---------------------------
@app.get("/")
async def root():
    return {"status": "running"}


# ============================================================
# GET /ebay/notifications/deletion  (challenge handshake)
# ============================================================
@app.get("/ebay/notifications/deletion")
async def ebay_deletion_challenge(
    challenge_code: str = Query(..., alias="challenge_code")
):
    """
    Handle eBay's validation challenge.

    eBay sends:
      GET /ebay/notifications/deletion?challenge_code=...

    We must respond with:
      {
        "challengeResponse": SHA256(challengeCode + verificationToken + endpointURL)
      }
    """

    # Build the string in EXACT order: challengeCode + verificationToken + endpointURL
    raw = f"{challenge_code}{VERIFICATION_TOKEN}{ENDPOINT_URL}"
    challenge_response = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    print("Received challenge_code:", challenge_code)
    print("Computed challengeResponse:", challenge_response)

    return {"challengeResponse": challenge_response}


# ============================================================
# POST /ebay/notifications/deletion  (real notifications)
# ============================================================

class EbayDeletionNotification(BaseModel):
    # We'll accept anything, but define a couple of common fields.
    # Extra JSON keys will be allowed.
    userId: str | None = None

    class Config:
        extra = "allow"


@app.post("/ebay/notifications/deletion")
async def ebay_deletion_handler(request: Request):
    """
    Handle actual deletion notifications from eBay.
    For now we just log the payload and ack.
    """
    data = await request.json()
    print("Received eBay deletion message:", data)
    return {"ack": "true"}

