all:
	@echo 'This is Make'

# Check unapplied migrations
checkmigrations:
	@python manage.py makemigrations --check --no-input --dry-run

# freeze packages
freeze:
	@pip freeze > ./requirements.txt

# make migrations and migrate
migrate:
	@python manage.py makemigrations && python manage.py migrate

# run install requirements
requirements:
	@pip install --upgrade pip
	@pip install -r requirements.txt

# run server 
server: 
	@python manage.py runserver

# run server 
server-with-checks: checkmigrations
	@python manage.py migrate && python manage.py runserver

# django shell
shell:
	@python manage.py shell
	
# create superuser
su:
	@python manage.py createsuperuser

# create virtual environment	
venv:
	@virtualenv .venv

# download chrome and chrome driver
.PHONY: chrome
chrome:
	wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chrome-linux64.zip
	mkdir -p chrome
	unzip chrome-linux64.zip -d chrome/temp
	mv chrome/temp/*/* chrome/
	rm chrome-linux64.zip
	rm -r chrome/temp

.PHONY: chrome-driver
chrome-driver:
	wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip
	unzip -j chromedriver-linux64.zip -d chrome/
	rm chromedriver-linux64.zip