MAP = maps/challenger/01_the_impossible_dream.txt

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