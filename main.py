import os
import re
import header.title

def get_public_url(log):
    match = re.search(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com", log)
    return match.group(0) if match else None

path = os.path.split(__file__)[0]
print(path)
os.system(f"nohup python server.py > server.log 2>&1 & ")
print("[*] Server started")
os.system(f"nohup cloudflared tunnel --url http://127.0.0.1:2374 > public_server.log 2>&1 & ")
print("[*] Cloudflared server started")
while True :
 with open(f"{path}/public_server.log", "r") as file :
      log = file.read()
 url = get_public_url(log)
 if url :
    break
with open("base_src/res/values/strings.xml", "r") as file :
     data = file.read()
     data = data.replace("server_url", url)
with open("base_src/res/values/strings.xml", "w") as file :
     file.write(data)
print("[*] Url added")
print("[*] Lunching controller")
os.system(f"python controller.py ")
