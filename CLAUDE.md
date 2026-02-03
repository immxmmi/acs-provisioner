# ACS Provisioner - Projektnotizen

## Architektur-Überblick

Pipeline-basiertes Provisioning-Tool für Red Hat ACS (Advanced Cluster Security / StackRox).
Liest YAML-Definitionen, führt Actions sequentiell aus und provisioniert Ressourcen über die ACS REST API.

## Datenfluss

```
settings.yaml + .env  →  Config (Singleton)
                              ↓
pipeline.yaml          →  PipelineReader.load_pipeline()
inputs.yaml            →  PipelineReader.load_inputs()
                              ↓
                         resolve_templates() → {{ key }} wird durch inputs-Werte ersetzt
                              ↓
                         PipelineValidator → prüft job-Namen gegen ACTION_REGISTRY
                              ↓
                         PipelineExecutor.run_pipeline()
                              ↓
                         Für jeden Step:
                           - params_list → iteriert über Liste aus inputs
                           - params      → einzelner Aufruf
                              ↓
                         Action.execute(data: dict) → ActionResponse
                              ↓
                         AcsGateway → ApiClient → ACS Central REST API
```

## Wichtige Dateien

| Komponente | Pfad |
|---|---|
| Entry Point | `src/main.py` |
| Config Loader | `src/config/loader.py` (Singleton, env > settings.yaml) |
| Settings | `src/config/settings.yaml` |
| Pipeline Engine | `src/engine/pipeline_engine.py` |
| Pipeline Reader | `src/engine_reader/pipeline_reader.py` |
| Pipeline Executor | `src/engine/pipeline_executor.py` |
| Action Registry | `src/engine/action_registry.py` (36+ Actions) |
| Pipeline Validator | `src/engine/pipeline_validator.py` |
| Base Action | `src/acs/actions/base_action.py` (abstrakte Klasse) |
| ACS Gateway | `src/acs/acs_gateway.py` (alle API-Methoden) |
| HTTP Client | `src/gateway/client.py` (Session, Auth, TLS) |
| Pipeline Definition | `src/pipelines/pipeline.yaml` |
| Pipeline Inputs | `src/pipelines/inputs.yaml` |
| Pydantic Models | `src/model/pipeline_model.py` (PipelineStep, PipelineDefinition) |

## Action-Struktur

Jede Ressource hat eigenen Ordner unter `src/acs/actions/<resource>/`:
- `create_*.py` - Erstellen/Upsert (create oder update wenn existiert)
- `get_*.py` - Einzelne Ressource holen + `find_by_name()`
- `list_*.py` - Alle Ressourcen auflisten
- `update_*.py` - Explizites Update (nur auth_provider hat das separat)
- `delete_*.py` - Löschen

Ressourcen: `notifier`, `auth_provider`, `role`, `access_scope`, `permission_set`, `integration`, `policy`

## Models

Jede Ressource hat ein Pydantic-Model unter `src/acs/model/`:
- `notifier/notifier.py` → `Notifier`
- `auth_provider_model.py` → `AuthProvider`
- `role_model.py` → `Role`
- `access_scope_model.py` → `AccessScope`
- `permission_set_model.py` → `PermissionSet`
- `integration_model.py` → `ImageIntegration`
- `policy_model.py` → `Policy`

Alle Models haben `to_api_payload()` das `id=None` Felder korrekt ausschließt.

## Gateway-Methoden (acs_gateway.py)

Für jede Ressource existieren: `list_*`, `get_*`, `create_*`, `update_*`, `delete_*`
- Meiste Updates nutzen `id` als Identifier
- **Ausnahme Role**: `update_role(role_name, payload)` nutzt den Namen statt ID

## Upsert-Logik (implementiert)

Alle 7 Create-Actions haben Upsert-Pattern:
```python
if existing:
    merged = {**existing, **data}   # Pipeline-Daten überschreiben Server-Daten
    model = Model(**merged)
    payload = model.to_api_payload()
    result = self.gateway.update_*(id_or_name, payload)
```

## Pipeline-Input-Mechanismus

- `params`: statische Werte direkt in pipeline.yaml
- `params_list: "{{ key }}"`: dynamische Liste aus inputs.yaml, wird pro Item iteriert
- Template-Auflösung in `PipelineReader.resolve_templates()`

## Besonderheiten

- Role hat extra Helper: `_resolve_permission_set(name)` und `_resolve_access_scope(name)` die per Gateway-Aufruf Name→ID auflösen
- HTTP Client unterstützt Bearer/Basic/API-Key Auth + TLS-Konfiguration
- Config ist Singleton: `Config()` gibt immer dieselbe Instanz zurück
