
run:
	docker compose up --build -d
	docker compose exec negotiation-app python worker.py