.PHONY: dev build install

dev:
	bash start.sh

build:
	bash build.sh

install:
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install
