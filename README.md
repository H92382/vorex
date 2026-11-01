```bash
termux-change-repo 
termux-setup-storage
cd /sdcard
pkg install git -y
git clone https://github.com/H92382/vorex
pkg install python -y
pkg install cloudflared -y 
pip install flask
pip install requests
cd vorex
python main.py 
```
