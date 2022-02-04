
.pipenv.timestamps: Pipfile.lock
	pipenv sync --dev
	pipenv install --skip-lock --editable .
	touch $@

.PHONY: prospector
prospector: .pipenv.timestamps
	pipenv run prospector --output=pylint

.PHONY: pyprest
pytest: .pipenv.timestamps
	pipenv run pytest --verbose --cov=jsonschema_gentypes -vv --cov-report=term-missing

.PHONY: jsonschema-gentypes
jsonschema-gentypes: .pipenv.timestamps
	pipenv run jsonschema-gentypes

.PHONY: build-docker
build-docker:
	docker build --tag=camptocamp/jsonschema-gentypes .
