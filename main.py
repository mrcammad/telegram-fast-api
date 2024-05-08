import telegram 
import settings
from fastapi import Query
from fastapi import Header
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()

class BotTelegram:
    def __init__(self):
        self.bot_token = settings.BOT_TOKEN
        self.chat_id = settings.CHAT_ID
        self.token = settings.TOKEN

    async def message(self, message):
        bot = telegram.Bot(token=self.bot_token)
        bot_message = await bot.send_message(chat_id=self.chat_id, text=message)
        return "enviado"
    
    def get_token(self):
        return self.token

bot = BotTelegram()


class MessageRequest(BaseModel):
    message: str


@app.get("/", include_in_schema=False)
def root():
    openapi_url = "/openapi.json"
    title = "API documentation"
    return get_swagger_ui_html(openapi_url=openapi_url, title=title)

@app.get("/openapi.json", include_in_schema=False)
def get_open_api_endpoint():
    return app.openapi()

@app.post("/send-message", tags=["Bot"])
async def send_message(message_request: MessageRequest, token: str = Header(None)):
    try:
        if token is None:
            raise HTTPException(status_code=400, detail="Token is missing. Please provide the token in the request headers.")
        
        elif token != bot.get_token():
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        elif token == bot.get_token():
            return await bot.message(message_request.message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-status", tags=["Bot"])
async def get_status(token: str = Query(..., title="Token", description="Token for authorization")):
    if token == bot.get_token():
        return {"status": "The bot is online"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

