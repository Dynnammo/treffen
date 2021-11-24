git clone https://github.com/Dynnammo/treffen.git && cd treffen
source ~/.env
apt-get update && apt-get -y dist-upgrade -y
apt-get install -y python3 python3-pip git
apt-get install -y poppler-utils 
apt-get install -y libsm6 libxext6 libxrender-dev
pip install -r requirements.txt
pip install gunicorn
python3 manage.py collectstatic
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn common.wsgi --bind=0.0.0.0:8000