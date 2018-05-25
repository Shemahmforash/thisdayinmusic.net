init:
	pip install pipenv
	pipenv install --dev
	cp thisdayinmusic/.env.example thisdayinmusic/.env
test:
	docker-compose run web sh -c "python manage.py test ${ARGS}"
