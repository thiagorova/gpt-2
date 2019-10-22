pyenv = python3.6
nosetest = $(pyenv) -m nose -s

run:
	export LC_ALL=en_US.UTF-8
	export LANG=en_US.UTF-8
	$(pyenv) src/server/app.py

setup:
	make deps
	$(pyenv) download_model.py 124M
	#$(pyenv) download_model.py 355M
	#$(pyenv) download_model.py 774M

deps:
	$(pyenv) -m pip install --upgrade pip
	$(pyenv) -m pip install --upgrade setuptools
	$(pyenv) -m pip install --upgrade -r requirements.txt

tests:
	#$(nosetest) src/tests/test_commons/test.py

test_handlers:
	$(nosetest) src/tests/test_handlers/*.py

clear:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
