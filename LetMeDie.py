from telethon import events
from .. import loader, utils
import os
import requests
from PIL import Image,ImageFont,ImageDraw
import re
import io
from textwrap import wrap

def register(cb):
 cb(JacquesThreeMod())

class JacquesThreeMod(loader.Module):
 """Загадка От LetMeDie"""
 strings = {
  'name': 'Загадка От LetMeDie',
  'usage': 'Ты Еблан? .let Текст или реплай',
 }
 def init(self):
  self.name = self.strings['name']
  self._me = None
  self._ratelimit = []
 async def client_ready(self, client, db):
  self._db = db
  self._client = client
  self.me = await client.get_me()

 async def letcmd(self, message):
  """да"""

  ufr = requests.get("https://raw.githubusercontent.com/LegushkaHacksGH/FTG-Stuff/main/open-sans.ttf?raw=true")
  f = ufr.content

  reply = await message.get_reply_message()
  args = utils.get_args_raw(message)
  if not args:
   if not reply:
    await utils.answer(message, self.strings('usage', message))
    return
   else:
    txt = reply.raw_text
  else:
   txt = utils.get_args_raw(message)
  await message.edit("<b>На Размышление 30 секунд...</b>")
  pic = requests.get("https://raw.githubusercontent.com/LegushkaHacksGH/FTG-Stuff/main/LetMeDie.jpg")
  pic.raw.decode_content = True
  img = Image.open(io.BytesIO(pic.content)).convert("RGB")

  W, H = img.size
  #txt = txt.replace("\n", "饟儛")
  text = "\n".join(wrap(txt, 20))
  t = text + "\n"
  #t = t.replace("饟儛","\n")
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype(io.BytesIO(f), 35, encoding='UTF-8')
  w, h = draw.multiline_textsize(t, font=font)
  imtext = Image.new("RGBA", (w+50, h+50), (0, 0,0,0))
  draw = ImageDraw.Draw(imtext)
  draw.multiline_text((40, 40),t,(225,225,225),font=font, align='left')
  imtext.thumbnail((450, 330))
  w, h = 604, 403
  img.paste(imtext, (2,100), imtext)
  out = io.BytesIO()
  out.name = "letmedie.jpg"
  img.save(out)
  out.seek(0)
  await message.client.send_file(message.to_id, out, reply_to=reply)
  await message.delete()