.PHONY: help install test ui api lint clean

# Default command when just running 'make'
help:
	@echo "🌍 AI Earth - The Intelligence Aggregator"
	@echo "----------------------------------------"
	@echo "Available commands:"
	@echo "  make install    - Install all dependencies (Core, UI, API, LEGOs)"
	@echo "  make ui         - Launch the Streamlit Master Control Dashboard"
	@echo "  make api        - Launch the FastAPI endpoint for the Intelligence Bus"
	@echo "  make test       - Run the validation suite for all LEGO pieces"
	@echo "  make lint       - Run Ruff for syntax checking"
	@echo "  make clean      - Remove __pycache__ and temp files"

install:
	@echo "Installing AI Earth requirements..."
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install ruff

ui:
	@echo "Igniting the Synapse Kernel UI..."
	streamlit run ai_earth/ui.py

api:
	@echo "Booting the OmniLog API..."
	# Adjust the path if the API entrypoint is different
	uvicorn ai_earth.api:app --reload

test:
	@echo "Running Singularity Tests..."
	pytest tests/ -v

lint:
	@echo "Linting with Ruff..."
	ruff check .

clean:
	@echo "Cleaning up temporary logic traces and cache..."
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
