# ============================================================================
#  ACS Provisioner - Makefile
# ============================================================================

PYTHON ?= python
SRC_DIR = src
VENV_DIR = .venv

# ============================================================================
#  Main Commands
# ============================================================================

.PHONY: help
help: ## Show this help
	@echo "ACS Provisioner - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Run the provisioner
	cd $(SRC_DIR) && $(PYTHON) main.py

.PHONY: run-debug
run-debug: ## Run with debug logging
	cd $(SRC_DIR) && LOG_LEVEL=DEBUG $(PYTHON) main.py

.PHONY: test
test: ## Run tests
	cd $(SRC_DIR) && $(PYTHON) -m pytest -v

.PHONY: test-models
test-models: ## Test model imports
	cd $(SRC_DIR)/acs/model && $(PYTHON) -c "from notifier import *; print('All notifier models OK')"

# ============================================================================
#  Setup
# ============================================================================

.PHONY: install
install: ## Install dependencies
	pip install -r requirements.txt

.PHONY: venv
venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Run: source $(VENV_DIR)/bin/activate"

.PHONY: setup
setup: venv ## Full setup (venv + install)
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Setup complete. Run: source $(VENV_DIR)/bin/activate"

# ============================================================================
#  Development
# ============================================================================

.PHONY: lint
lint: ## Run linter
	$(PYTHON) -m flake8 $(SRC_DIR) --max-line-length=120

.PHONY: format
format: ## Format code with black
	$(PYTHON) -m black $(SRC_DIR)

.PHONY: typecheck
typecheck: ## Run type checker
	$(PYTHON) -m mypy $(SRC_DIR)

.PHONY: clean
clean: ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# ============================================================================
#  Docker
# ============================================================================

IMAGE_NAME ?= acs-provisioner
TAG ?= latest

.PHONY: build
build: ## Build Docker image
	docker build -t $(IMAGE_NAME):$(TAG) .

.PHONY: docker-run
docker-run: ## Run in Docker
	docker run --rm --env-file .env -v $(PWD)/src/pipelines:/app/pipelines $(IMAGE_NAME):$(TAG)

# ============================================================================
#  RHACS Environment (Minikube)
# ============================================================================

ROXCTL ?= ./roxctl
STACKROX_NS ?= stackrox
CLUSTER_NAME ?= minikube

.PHONY: env-up
env-up: ## Start Minikube with ACS
	@command -v kubectl >/dev/null || { echo "kubectl missing"; exit 1; }
	@command -v minikube >/dev/null || { echo "minikube missing"; exit 1; }
	minikube start --cpus=4 --memory=8g --disk-size=40g --driver=docker
	kubectl create namespace $(STACKROX_NS) || true
	$(ROXCTL) central generate k8s yaml --password admin > central.yaml
	kubectl apply -f central.yaml
	kubectl -n $(STACKROX_NS) rollout status deploy/central
	$(ROXCTL) secured-cluster generate k8s yaml --cluster-name $(CLUSTER_NAME) > secured.yaml
	kubectl apply -f secured.yaml

.PHONY: env-down
env-down: ## Stop Minikube
	minikube delete

.PHONY: env-status
env-status: ## Show ACS pod status
	kubectl -n $(STACKROX_NS) get pods

.PHONY: env-ui
env-ui: ## Port-forward ACS UI (https://localhost:8443)
	kubectl -n $(STACKROX_NS) port-forward svc/central 8443:443

.PHONY: roxctl
roxctl: ## Download roxctl CLI
	@if [ ! -f $(ROXCTL) ]; then \
	  curl -L -o $(ROXCTL) https://mirror.openshift.com/pub/rhacs/assets/latest/bin/darwin/roxctl; \
	  chmod +x $(ROXCTL); \
	fi
