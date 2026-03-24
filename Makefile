run: .venv app.py
	.venv/bin/python3 app.py

dist: .venv app.py
	.venv/bin/pyinstaller app.py --onefile --add-data ./index.html:. --name tim

clean:
	@rm -rf -- dist

distclean: clean
	@rm -rf .venv build tim.spec

.venv:
	python3 -m venv $@
	$@/bin/pip install Flask pyinstaller

.PHONY: dist run
