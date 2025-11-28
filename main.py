from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


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
    # eBay may also send userId, reason, or other fields
    # We accept them but don't require them
    # using **kwargs in the POST route


@app.post("/ebay/notifications/deletion")
async def ebay_deletion_handler(request: Request):

    data = await request.json()

    # 1: Handle eBay Challenge handshake
    if "challengeCode" in data:
        return {"challengeResponse": data["challengeCode"]}

    # 2: Log the message (for now)
    print("Received eBay deletion message:", data)

    # 3: Acknowledge
    return {"ack": "true"}

