.PHONY: install setup test run-api run-dashboard clean

install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

setup:
	cp .env.example .env
	python scripts/setup_db.py

test:
	pytest tests/ -v --cov=src

run-api:
	uvicorn src.api.main:app --reload --port 8000

run-dashboard:
	streamlit run src/dashboard/app.py --server.port 8501

run-ingestion:
	python scripts/run_ingestion.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
