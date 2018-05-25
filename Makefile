init:
	docker-compose up -d

test:
	docker-compose run dev sh -c "python manage.py test ${ARGS}"
