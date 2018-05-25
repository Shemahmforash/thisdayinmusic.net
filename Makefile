init:
	docker-compose up -d

test:
	docker-compose run dev sh -c "python manage.py test ${ARGS}"

.PHONY: manage
manage:
	docker-compose run --entrypoint "python manage.py ${ARGS}" web
