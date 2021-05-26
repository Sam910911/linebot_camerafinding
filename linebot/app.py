from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('w7B99HN+7osyW67qlqaiJsFn/TdDcY9alQpDr2DJVJDF2Dsx0vRqdaYztyuT5OUt262ZBaFJcQD6xX1WFoUSeMEvK4ot2ASvjM/Mo1QiLAc7ZX6vh7VwdCzjQdbLUvWdGP9fzZ4IvzdoQ53Ai0LSAQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c13718c8c046358a4cb9989c40644846')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    search = event.message.text
    url = 'https://www.dcfever.com/cameras/keywordsearch.php?gadgetkeyword='+search+'&form_action=search_action&search_btn=%E6%90%9C%E5%B0%8B'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    item = soup.find_all('div',{'class':'gadget_div onefourth'})
    output = ''
    for i in range(0,5):
        try:
            if i == 5:
                links = item[i].find_all('a')
                link = links[0].get('href')
                output += 'https://www.dcfever.com/' + link
            else:
                links = item[i].find_all('a')
                link = links[0].get('href')
                output += 'https://www.dcfever.com/' + link + '\n'
        except:
            output += "end of search"
            break
    message = TextSendMessage(text=output)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
