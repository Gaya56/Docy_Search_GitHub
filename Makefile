.PHONY: build run stop test clean logs health

# Build the container
build:
	@echo "🔨 Building Tool Recommendation Container..."
	docker-compose build

# Run the container
run:
	@echo "🚀 Starting Tool Recommendation Container..."
	docker-compose up -d
	@echo "✅ Container started! Access at http://localhost:8947"

# Stop the container
stop:
	@echo "🛑 Stopping Tool Recommendation Container..."
	docker-compose down

# Test the container
test:
	@echo "🧪 Testing Tool Recommendation Container..."
	python test_container.py

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f

# View logs
logs:
	@echo "📋 Viewing container logs..."
	docker-compose logs -f

# Health check
health:
	@echo "🏥 Checking container health..."
	curl -f http://localhost:8947/health || echo "❌ Container not healthy"

# Full setup and test
setup: build run
	@echo "⏳ Waiting for container to start..."
	@sleep 10
	@make test

# Development mode (with live reload)
dev:
	@echo "🔧 Starting in development mode..."
	uvicorn server:app --host 0.0.0.0 --port 8947 --reload
