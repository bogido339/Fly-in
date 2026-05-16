MAP = maps/challenger/01_the_impossible_dream.txt

PYTHON = python3
MAIN = main.py

install:
	$(PYTHON) -m pip install flake8 mypy poetry

run:
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .

lint-strict:
	flake8 . --max-line-length=88 --statistics
	mypy .

.PHONY: install run debug clean lint lint-strict