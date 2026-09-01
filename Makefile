# Makefile to manage library backend and frontend development environment

# Configuration
PYTHON = myvenv/bin/python3
FRONTEND_DIR = frontend

.PHONY: help run run-backend run-frontend install build clean

help:
	@echo "Available commands:"
	@echo "  make run          - Run backend and frontend concurrently (Ctrl+C to stop both)"
	@echo "  make run-backend  - Run the FastAPI backend server only"
	@echo "  make run-frontend - Run the React Vite frontend server only"
	@echo "  make install      - Install dependencies for the frontend"
	@echo "  make build        - Compile the frontend production build"
	@echo "  make clean        - Remove compiled frontend build files"

run:
	@echo "Starting FastAPI backend and React frontend concurrently..."
	@trap 'kill 0' INT; \
	$(PYTHON) runserver.py & \
	npm run dev --prefix $(FRONTEND_DIR) & \
	wait

run-backend:
	$(PYTHON) runserver.py

run-frontend:
	npm run dev --prefix $(FRONTEND_DIR)

install:
	@echo "Installing frontend dependencies..."
	npm install --prefix $(FRONTEND_DIR)

build:
	npm run build --prefix $(FRONTEND_DIR)

clean:
	rm -rf $(FRONTEND_DIR)/dist
