from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DeleteRequest(BaseModel):
    itemId: str

@app.post("/delete")
async def delete_item(data: DeleteRequest):
    print("============ eBay Delete Webhook ============")
    print("Item:", data.itemId)
    print("=============================================")
    return {"ack": "true"}

@app.get("/")
async def root():
    return {"status": "running"}