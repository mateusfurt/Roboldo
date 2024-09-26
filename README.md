# Roboldo
Robô social da UERN-NATAL

git clone -b ROBOLDO-IA https://github.com/mateusfurt/Roboldo.git


python -m venv chat-roboldo

Ativar no windows:
chat-roboldo\Scripts\activate

Ativar linux:
source chat-roboldo/bin/activate

desativar:
deactivate

pip install -r requirements.txt

Ativar API key no terminal:
Windows:
setx OPENAI_API_KEY "your_api_key_here"
Linux:
export OPENAI_API_KEY="your_api_key_here"

python voice.py/button.py
ou
python3 voice.py/button.py