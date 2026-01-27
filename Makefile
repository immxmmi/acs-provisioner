# ============================================================================
#  RHACS Environment Setup - Makefile
# ============================================================================

ROXCTL ?= ./roxctl
STACKROX_NS ?= stackrox
CLUSTER_NAME ?= minikube

up:
	@command -v kubectl >/dev/null || { echo "kubectl missing"; exit 1; }
	@command -v minikube >/dev/null || { echo "minikube missing"; exit 1; }

	minikube start --cpus=4 --memory=8g --disk-size=40g --driver=docker

	kubectl create namespace $(STACKROX_NS) || true

	$(ROXCTL) central generate k8s yaml \
	  --password admin > central.yaml
	kubectl apply -f central.yaml
	kubectl -n $(STACKROX_NS) rollout status deploy/central

	$(ROXCTL) secured-cluster generate k8s yaml \
	  --cluster-name $(CLUSTER_NAME) > secured.yaml
	kubectl apply -f secured.yaml

down:
	minikube delete

status:
	kubectl -n $(STACKROX_NS) get pods

ui:
	kubectl -n $(STACKROX_NS) port-forward svc/central 8443:443

roxctl:
	@if [ ! -f $(ROXCTL) ]; then \
	  curl -L -o $(ROXCTL) https://mirror.openshift.com/pub/rhacs/assets/latest/bin/darwin/roxctl; \
	  chmod +x $(ROXCTL); \
	fi