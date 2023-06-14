.ONESHELL:

check: setstyle static
	 . ./venv/bin/activate
	 pyflakes python3

venv: requirements.txt
	rm -rf venv
	virtualenv -p python3 venv
	. ./venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt

style: venv
	. ./venv/bin/activate
	black --check python3
	flake8 python3

setstyle: venv
	. ./venv/bin/activate
	black python3
	flake8 python3

build.touch: venv
	. ./venv/bin/activate
	pip install -e .
	touch build.touch

static: venv
	. ./venv/bin/activate
	pyright python3

.PHONY: style setstyle check static
