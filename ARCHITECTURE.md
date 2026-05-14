# KesselFlow Architecture Map
**Generated:** 2026-05-13 16:26
**Tree version:** 1.0
**Root:** KesselFlow

---

## AGENTS
### ARES
- **type:** agent
- **log:** ~/kesselflow/logs/ares.log
- **liveness:** unknown
- **heartbeat_file:** ~/.locks/ares.heartbeat

### FENRIS
- **type:** agent
- **log:** ~/kesselflow/logs/fenris.log
- **liveness:** unknown
- **heartbeat_file:** ~/.locks/fenris.heartbeat

### CERBERUS
- **type:** agent
- **log:** ~/kesselflow/logs/cerberus.log
- **liveness:** unknown
- **heartbeat_file:** ~/.locks/cerberus.heartbeat

### INQUISITOR
- **type:** agent
- **log:** ~/kesselflow/logs/inquisitor.log
- **role:** json_logger
- **output:** log.jsonl
- **liveness:** unknown
- **heartbeat_file:** ~/.locks/inquisitor.heartbeat

## BONEYARD
### sop_sync
- **type:** script
- **path:** ~/kesselflow/scripts/sop_sync.sh
- **schedule:** 0 3 * * *
- **input:** ~/kesselflow/current_state.json
- **output:** /sdcard/boneyard/KesselFlow/SOPs/master_state.json
- **delta_archive:** /sdcard/boneyard/KesselFlow/SOPs/history/

### BoneYard store
- **type:** storage
- **path:** /sdcard/boneyard/KesselFlow/SOPs/
- **log:** /sdcard/boneyard/logs/sop_delta.log

## ORCHESTRATION
### KesselOrchestratorV2
- **type:** pipeline
- **path:** ~/kesselflow/scripts/orchestrator.py
- **components:** WhitelistGate, SearchCoordinator
- **audit_output:** ./tasks/audit_log.json

### kessel_learn
- **type:** learner
- **path:** ~/kesselflow/kessel_learn.py
- **schedule:** nightly
- **input:** agent trace logs
- **output:** ~/kesselflow/CLAUDE.md

## STATE
### current_state
- **type:** state_file
- **path:** ~/kesselflow/current_state.json
- **symlink:** ~/.kessel_state.json

### handoff
- **type:** continuity_doc
- **path:** ~/kesselflow/handoff.json

### EXXACT-KF-2.0
- **type:** frozen_profile
- **path:** ~/kesselflow/kessel_state_exxact.json
- **guard:** NO_POC/EXEC
- **review_date:** 2027-05-12

## SECURITY
### WhitelistGate
- **type:** security_layer
- **model:** Positive Security Model
- **action:** TOKEN_OUT_OF_SCOPE replacement
- **telemetry:** ./tasks/audit_log.json

### OPA auditor
- **type:** policy_engine
- **scope:** agent ops

### FROZEN_WEIGHTS
- **type:** protocol
- **guard:** LIFO_GATING + TRUTH_OR_FAILURE + SEMANTIC_DIFF

---

## SLASH COMMANDS

| Command | Scope | Description |
|---|---|---|
| `/devil` | adversarial | Stress-test KesselFlow config for failure modes, attack surf... |
| `/wiki` | documentation | Generate documentation, command registry, or architecture ma... |
| `/10x` | automation | Productivity multiplier — automate all KF maintenance into a... |
| `/scout` | reconnaissance | Drift detection, system survey, and agent liveness scanning.... |
| `/godmode` | activation | Full system activation — all agents, monitors, sync, and hea... |
| `/ooda` | strategy | Observe-Orient-Decide-Act cycle against current KesselFlow s... |

### `/devil`
- **scope:** adversarial
- **description:** Stress-test KesselFlow config for failure modes, attack surface review, and devil's advocate architecture challenges.
- **modes:**
  - `1` — adversarial_audit: Stress-test current KesselFlow config for failure modes
  - `2` — red_team: Attack surface review on orchestrator/WhitelistGate
  - `3` — devils_advocate: Argue against current architecture decisions

### `/wiki`
- **scope:** documentation
- **description:** Generate documentation, command registry, or architecture map from live KesselFlow state.
- **modes:**
  - `1` — generate_docs: Full markdown wiki for KesselFlow
  - `2` — command_registry: Document all registered slash commands
  - `3` — architecture_map: Human-readable system overview from workflow_tree.json

### `/10x`
- **scope:** automation
- **description:** Productivity multiplier — automate all KF maintenance into a single master script.
- **modes:**
  - `1` — sprint_mode: Identify next 10 highest-value KF improvements
  - `2` — automate_self: Generate master maintenance script kf_maintain.py
  - `3` — compound_session: Chain /scout + /devil + /godmode into one command

### `/scout`
- **scope:** reconnaissance
- **description:** Drift detection, system survey, and agent liveness scanning.
- **modes:**
  - `1` — system_survey: Inventory all KesselFlow files, sizes, ages
  - `2` — drift_detection: Compare current_state.json against master_state.json
  - `3` — dead_process_scan: Check agent heartbeat files for liveness

### `/godmode`
- **scope:** activation
- **description:** Full system activation — all agents, monitors, sync, and heartbeats in sequence.
- **modes:**
  - `1` — full_activation: Start all agents + monitors + sop_sync in sequence
  - `2` — system_hardening: Run all /devil fixes + /scout drift check
  - `3` — emperor_mode: Generate master control script wrapping all KF commands

### `/ooda`
- **scope:** strategy
- **description:** Observe-Orient-Decide-Act cycle against current KesselFlow state.

---

## CRON SCHEDULE

| Time  | Script | Purpose |
|---|---|---|
| 03:00 | `sop_sync.sh` | BoneYard delta sync |
| 04:00 | `kf_maintain.py` | Full system maintenance |

---

## INVARIANTS

- No /tmp — use ~/.locks/
- No pkg upgrade — MongoDB pinned
- No PM2/lsof/ss/fuser
- Logs to ~/kessel_live/logs/ or ~/kesselflow/logs/
- File writes via python3 <<'PYEOF' blocks only
- printf '\e[?2004l' before every multi-line paste
- Do not merge Donny outputs without explicit user confirmation
- No prose after final code block in terminal context

---

*Infrastructure that doesn't need a babysitter.*