venv_dir ?= .venv


.PHONY: all
all: build tools

.PHONY: build
build: $(venv_dir)

.PHONY: run
run: build
	$(venv_dir)/bin/flask \
		--debug --app app.py \
		run \
			--host 'localhost' --port 8090

$(venv_dir): requirements.txt
	python -m venv $(venv_dir)
	$(venv_dir)/bin/pip install --upgrade pip
	$(venv_dir)/bin/pip install -r requirements.txt && touch $(@)

$(venv_dir)/bin/%: | $(venv_dir)
	$(venv_dir)/bin/pip install $(@F)


.PHONY: tools
tools: \
	$(venv_dir) \
	$(venv_dir)/bin/black \
	$(venv_dir)/bin/isort

.PHONY: black
black: $(venv_dir)/bin/black
	$(venv_dir)/bin/black app.py

.PHONY: isort
isort: $(venv_dir)/bin/isort
	$(venv_dir)/bin/isort ./app.py --atomic

docs/build:
	mkdir -p $(@)

docs/build/html: docs/build
	mkdir -p $(@)

.PHONY: clean
clean:
	test ! -d '$(venv_dir)' || rm -rf '$(venv_dir)'
