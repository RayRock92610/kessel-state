#!/bin/bash
set -euo pipefail

BY_PATH="/sdcard/boneyard/KesselFlow/SOPs"
LOG_DIR="/sdcard/boneyard/logs"
LOG_PATH="${LOG_DIR}/sop_delta.log"
CURRENT="$HOME/kesselflow/current_state.json"
MASTER="${BY_PATH}/master_state.json"
HISTORY_DIR="${BY_PATH}/history"
TIMESTAMP=$(date +%Y-%m-%d_%H%M)

mkdir -p "$LOG_DIR" "$HISTORY_DIR"

if [ ! -d "$BY_PATH" ]; then
  echo "[${TIMESTAMP}] ERROR: BoneYard not mounted at ${BY_PATH}" | tee -a "$LOG_PATH"
  exit 1
fi

if ! touch /sdcard/boneyard/.healthcheck 2>/dev/null; then
  echo "[${TIMESTAMP}] ERROR: /sdcard not writable — aborting sync" | tee -a "$LOG_PATH"
  exit 1
fi
rm -f /sdcard/boneyard/.healthcheck

if [ ! -f "$CURRENT" ]; then
  echo "[${TIMESTAMP}] ERROR: current_state.json missing at ${CURRENT}" | tee -a "$LOG_PATH"
  exit 1
fi

if [ ! -f "$MASTER" ]; then
  cp "$CURRENT" "$MASTER"
  echo "[${TIMESTAMP}] Initialized master_state.json from local copy" >> "$LOG_PATH"
fi

TMP_DIFF="$HOME/.locks/sop_delta_${TIMESTAMP}.diff"
mkdir -p "$HOME/.locks"
diff -q "$CURRENT" "$MASTER" > "$TMP_DIFF" 2>&1
DIFF_RC=$?

if [ "$DIFF_RC" -eq 0 ]; then
  echo "[${TIMESTAMP}] No drift detected. Veracity 100%." >> "$LOG_PATH"
  rm -f "$TMP_DIFF"
elif [ "$DIFF_RC" -eq 1 ]; then
  echo "[${TIMESTAMP}] Delta detected. Updating BoneYard SOPs." >> "$LOG_PATH"
  cp "$CURRENT" "$MASTER"
  cat "$TMP_DIFF" >> "${HISTORY_DIR}/delta_${TIMESTAMP}.log"
  rm -f "$TMP_DIFF"
else
  echo "[${TIMESTAMP}] ERROR: diff failed RC=${DIFF_RC}" | tee -a "$LOG_PATH"
  rm -f "$TMP_DIFF"
  exit 1
fi

echo "[${TIMESTAMP}] sop_sync complete." >> "$LOG_PATH"
