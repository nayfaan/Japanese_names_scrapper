cd "$(dirname "$0")"

source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

clear
python3 main.py
