# =========================
# RHACS local dev Makefile
# =========================

MINIKUBE_CPUS   ?= 4
MINIKUBE_MEMORY ?= 8g
MINIKUBE_DISK   ?= 40g
MINIKUBE_DRIVER ?= docker

ROXCTL          ?= ./roxctl
STACKROX_NS     ?= stackrox
CLUSTER_NAME    ?= minikube

.PHONY: help up down status ui api roxctl

help:
	@echo ""
	@echo "Targets:"
	@echo "  make up        Start minikube + install RHACS"
	@echo "  make down      Delete minikube cluster"
	@echo "  make status    Show RHACS pods"
	@echo "  make ui        Port-forward Central UI/API"
	@echo "  make api       Test ACS API"
	@echo ""

# -------------------------
# Cluster
# -------------------------
up: roxctl
	minikube start \
	  --cpus=$(MINIKUBE_CPUS) \
	  --memory=$(MINIKUBE_MEMORY) \
	  --disk-size=$(MINIKUBE_DISK) \
	  --driver=$(MINIKUBE_DRIVER)

	kubectl create namespace $(STACKROX_NS) || true

	$(ROXCTL) central generate k8s yaml \
	  --output central.yaml \
	  --password admin

	kubectl apply -f central.yaml
	kubectl -n $(STACKROX_NS) rollout status deploy/central

	$(ROXCTL) secured-cluster generate k8s yaml \
	  --output secured.yaml \
	  --cluster-name $(CLUSTER_NAME)

	kubectl apply -f secured.yaml

	@echo "RHACS ready."

down:
	minikube delete

status:
	kubectl -n $(STACKROX_NS) get pods

ui:
	kubectl -n $(STACKROX_NS) port-forward svc/central 8443:443

api:
	@echo "Example:"
	@echo "curl -k -H \"Authorization: Bearer <TOKEN>\" https://localhost:8443/v1/policies"

# -------------------------
# Tools
# -------------------------
roxctl:
	@if [ ! -f $(ROXCTL) ]; then \
	  echo "Downloading roxctl..."; \
	  curl -L -o $(ROXCTL) https://mirror.openshift.com/pub/rhacs/assets/latest/bin/darwin/roxctl; \
	  chmod +x $(ROXCTL); \
	fi