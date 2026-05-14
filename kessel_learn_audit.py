import os
import json
import datetime

def mine_audit_log(audit_path, claude_md_path):
    audit_path = os.path.expanduser(audit_path)
    claude_md_path = os.path.expanduser(claude_md_path)

    if not os.path.exists(audit_path):
        print(f"[LEARN] audit_log not found at {audit_path} — skipping")
        return

    blocked_tokens = []
    MAX_LINES = 1000
    with open(audit_path) as f:
        for i, line in enumerate(f):
            if i >= MAX_LINES: break
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if "blocked" in entry:
                    blocked_tokens.append(entry["blocked"])
            except json.JSONDecodeError:
                continue

    if os.path.exists(claude_md_path) and os.path.getsize(claude_md_path) > 500_000:
        print("[LEARN] CLAUDE.md exceeds 500KB — skipping append")
        return
    if not blocked_tokens:
        print("[LEARN] No blocked tokens in audit_log — nothing to mine")
        return

    summary = (
        f"\n## Audit Log Mining — {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
        f"- Source: {audit_path}\n"
        f"- Blocked tokens ({len(blocked_tokens)}): {', '.join(set(blocked_tokens))}\n"
        f"- Action: Review whitelist coverage.\n"
    )

    lock_path = claude_md_path + ".lock"
    if os.path.exists(lock_path):
        print("[LEARN] CLAUDE.md locked — skipping")
        return
    open(lock_path, "w").close()
    try:
        with open(claude_md_path, "a") as f:
            f.write(summary)
    finally:
        os.remove(lock_path)

    print(f"[LEARN] {len(blocked_tokens)} blocked token(s) mined — appended to CLAUDE.md")

if __name__ == "__main__":
    mine_audit_log(
        audit_path="/data/data/com.termux/files/home/kesselflow/scripts/tasks/audit_log.json",
        claude_md_path="~/kesselflow/CLAUDE.md"
    )
