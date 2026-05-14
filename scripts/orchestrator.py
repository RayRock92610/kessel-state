import os
import datetime
import json

class WhitelistGate:
    def __init__(self, allowed_vocab):
        self.whitelist = set(word.lower() for word in allowed_vocab)
        self.audit_log = []

    def enforce(self, text):
        words = text.split()
        sanitized = []
        for word in words:
            clean = "".join(filter(str.isalnum, word)).lower()
            if len(clean) < 2 or clean in self.whitelist or not clean:
                sanitized.append(word)
            else:
                self.audit_log.append({
                    "timestamp": str(datetime.datetime.now()),
                    "blocked": word
                })
                sanitized.append("[TOKEN_OUT_OF_SCOPE]")
        return " ".join(sanitized)

class SearchCoordinator:
    def sanitize_query(self, query, tech_keywords):
        words = query.split()
        filtered = [w for w in words if w.lower() in tech_keywords]
        return " ".join(filtered) if filtered else "security infrastructure updates"

class KesselOrchestratorV2:
    def __init__(self, vocab, workspace="/data/data/com.termux/files/home/kesselflow/scripts/tasks"):
        self.workspace = workspace
        self.gate = WhitelistGate(vocab)
        self.coordinator = SearchCoordinator()
        self.audit_file = os.path.join(self.workspace, "audit_log.json")
        os.makedirs(self.workspace, exist_ok=True)

    def execute_flow(self, intent):
        clean_intent = self.gate.enforce(intent)
        sanitized_search = self.coordinator.sanitize_query(
            clean_intent, self.gate.whitelist
        )
        with open(self.audit_file, "a") as f:
            for entry in self.gate.audit_log:
                f.write(json.dumps(entry) + "\n")
        self.gate.audit_log.clear()
        print(f"[KF-V2] Intent sanitized: \'{clean_intent}\'")
        print(f"[KF-V2] Search redirected to: \'{sanitized_search}\'")
        print(f"[KF-V2] Observability Active: audit written to {self.audit_file}")

if __name__ == "__main__":
    tech_vocab = [
        "python", "bash", "termux", "audit", "api", "security",
        "git", "kessel", "infrastructure", "encryption"
    ]
    orchestrator = KesselOrchestratorV2(tech_vocab)
    orchestrator.execute_flow("Automate the security audit for the internal API")
