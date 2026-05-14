#!/usr/bin/env python3
import os, json, subprocess, datetime, hashlib

PATHS = {
    "sop_sync":      "~/kesselflow/scripts/sop_sync.sh",
    "orchestrator":  "~/kesselflow/scripts/orchestrator.py",
    "workflow_tree": "~/kesselflow/scripts/workflow_tree.json",
    "handoff":       "~/kesselflow/handoff.json",
    "learn_audit":   "~/kesselflow/kessel_learn_audit.py",
    "exxact":        "~/kesselflow/kessel_state_exxact.json",
    "kessel_state":  "~/.kessel_state.json",
    "claude_md":     "~/kesselflow/CLAUDE.md",
    "current_state": "~/kesselflow/current_state.json",
    "master_state":  "/sdcard/boneyard/KesselFlow/SOPs/master_state.json",
}
AGENTS = ["ares","fenris","cerberus","inquisitor"]
LOCKS  = os.path.expanduser("~/.locks")
LOG    = os.path.expanduser("~/kesselflow/logs/kf_maintain.log")
os.makedirs(LOCKS, exist_ok=True)
os.makedirs(os.path.dirname(LOG), exist_ok=True)

def log(msg):
    line = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(LOG,"a") as f: f.write(line+"\n")

def fhash(p):
    p=os.path.expanduser(p)
    if not os.path.exists(p): return None
    with open(p,"rb") as f: return hashlib.blake2b(f.read()).hexdigest()[:16]

def run(cmd): return subprocess.run(cmd,capture_output=True,text=True)

report={}
ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
log("="*50)
log("KF MAINTENANCE — FULL RUN")
log("="*50)

log("[STEP 1] Integrity check")
missing=[n for n,r in PATHS.items() if not os.path.exists(os.path.expanduser(r))]
for n,r in PATHS.items():
    log(f"  [{'MISSING' if n in missing else 'OK'}] {n}")
report["integrity"]="FAIL" if missing else "PASS"

log("[STEP 2] BoneYard sync")
r=run(["bash",os.path.expanduser(PATHS["sop_sync"])])
report["sop_sync"]="PASS" if r.returncode==0 else "FAIL"
log(f"  [{'OK' if r.returncode==0 else 'FAIL'}] sop_sync rc={r.returncode}")

log("[STEP 3] Drift scan")
ch=fhash(PATHS["current_state"]); mh=fhash(PATHS["master_state"])
if ch and mh and ch==mh:
    log(f"  [OK] IN SYNC hash={ch}"); report["drift"]="PASS"
elif ch and mh:
    log(f"  [DRIFT] current={ch} master={mh}"); report["drift"]="DRIFT"
else:
    log(f"  [WARN] current={ch or 'MISSING'} master={mh or 'MISSING'}"); report["drift"]="WARN"

log("[STEP 4] KesselOrchestratorV2")
r=run(["python3",os.path.expanduser(PATHS["orchestrator"])])
for line in r.stdout.strip().split("\n"): log(f"  {line}")
report["orchestrator"]="PASS" if r.returncode==0 else "FAIL"

log("[STEP 5] Audit mining")
r=run(["python3",os.path.expanduser(PATHS["learn_audit"])])
for line in r.stdout.strip().split("\n"): log(f"  {line}")
report["kessel_learn"]="PASS" if r.returncode==0 else "FAIL"

log("[STEP 6] Heartbeats")
for agent in AGENTS:
    hb=os.path.join(LOCKS,f"{agent}.heartbeat")
    with open(hb,"w") as f: f.write(ts)
    log(f"  [OK] {agent}.heartbeat")
report["heartbeats"]="PASS"

log("[REPORT]")
for k,v in report.items(): log(f"  {k:<20} {v}")
all_pass=all(v=="PASS" for v in report.values())
log(f"[STATUS] {'FULLY ACTIVE' if all_pass else 'PARTIAL'}")
log("="*50)
