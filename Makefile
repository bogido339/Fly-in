MAP = maps/easy/01_linear_path.txt

install:
	pip install flake8 mypy poetry

run:
	python3 main.py $(MAP)

debug:
	python3 -m pdb fly-in.py

clean:
	
lint:

lint-strict:
	

.PHONY: install run debug clean lint lint-strict