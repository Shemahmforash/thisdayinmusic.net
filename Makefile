init:
	pip install pipenv
	pipenv install --dev
	cp thisdayinmusic/.env.example thisdayinmusic/.env
test:
	pipenv run python manage.py test
