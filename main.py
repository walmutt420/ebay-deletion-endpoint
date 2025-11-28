from fastapi import FastAPI, Request

app = FastAPI()

# Your verification token
VERIFICATION_TOKEN = "12345678901234567890123456789012"

@app.get("/")
async def home():
    return {"status": "running"}

# ---------------------------
# Marketplace Account Deletion
# ---------------------------

@app.get("/ebay/notifications/deletion")
async def ebay_deletion_get(challenge_code: str = None):
    """
    eBay GET challenge handshake.
    Must return the SAME challenge_code back.
    """
    if challenge_code:
        return {"challengeResponse": challenge_code}
    return {"status": "ok"}

@app.post("/ebay/notifications/deletion")
async def ebay_deletion_post(request: Request):
    """
    eBay POST notification.
    They may include challengeCode here as well.
    """
    data = await request.json()

    # If POST includes a challengeCode, return it back
    if "challengeCode" in data:
        return {"challengeResponse": data["challengeCode"]}

    # Otherwise just ACK the notification
    print("Received deletion notification:", data)
    return {"ack": "true"}
