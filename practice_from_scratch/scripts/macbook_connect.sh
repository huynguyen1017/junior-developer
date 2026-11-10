#!/usr/bin/env bash
# ==============================================================================
# ENGR 852 Studio v7.0 — Evidence-Integrity Multi-Mac Setup & Capability Helper
# ==============================================================================
# IMPORTANT v7.0 POLICY:
# - Never installs fake Synopsys binary shims (`vcs`, `verdi`, `fc_shell`, `icv`, `pt_shell`)
#   that impersonate real Synopsys licenses or fabricate `PASS` / `CLEAN` outputs!
# - Removes any legacy `~/.engr852_eda_bin` fake tool wrappers if present.
# - Sets up local non-secret user identity (`~/.config/engr852/user_identity.txt`)
#   and starts the local v7.0 studio server on `127.0.0.1:8788`.
# ==============================================================================
set -e

echo "================================================================================"
echo "🛡️ [ENGR 852 Studio v7.0] Evidence-Integrity Local Setup & Multi-Mac Sync"
echo "   Host: $(whoami)@$(hostname) | Date: $(date)"
echo "================================================================================"

# 1. Remove any legacy v5/v6 fake EDA binary shims in ~/.engr852_eda_bin so local shell
#    commands NEVER impersonate Synopsys VCS/Verdi/FusionCompiler/ICV/PrimeTime!
EDA_BIN="$HOME/.engr852_eda_bin"
if [ -d "$EDA_BIN" ]; then
  for fake_tool in vcs verdi fc_shell icv pt_shell; do
    if [ -f "$EDA_BIN/$fake_tool" ]; then
      rm -f "$EDA_BIN/$fake_tool"
      echo "  [✓] Removed legacy fake EDA shim: $EDA_BIN/$fake_tool"
    fi
  done
fi

# Provide only standard sha256sum -> shasum -a 256 utility if missing on macOS
mkdir -p "$EDA_BIN"
cat << 'EOF_SHA' > "$EDA_BIN/sha256sum"
#!/usr/bin/env bash
shasum -a 256 "$@"
EOF_SHA
chmod +x "$EDA_BIN/sha256sum"

# 2. Locate repository
REPO_DIR=""
for candidate in \
  "$HOME/Developer/portfolio/motion-estimator-asic-lab-notebook-2026" \
  "$HOME/motion-estimator-asic-lab-notebook-2026" \
  "$HOME/Developer/engr852_practice/motion-estimator-asic-lab-notebook-2026"; do
  if [ -d "$candidate/.git" ]; then
    REPO_DIR="$candidate"
    break
  fi
done

if [ -n "$REPO_DIR" ]; then
  echo "  [•] Found repository at: $REPO_DIR"
  ID_SCRIPT="$REPO_DIR/practice_from_scratch/scripts/engr852_identity_setup.py"
  if [ -f "$ID_SCRIPT" ]; then
    python3 "$ID_SCRIPT" --status || true
  fi
fi

echo "================================================================================"
echo "✅ v7.0 Evidence-Integrity Environment Ready (No fake EDA shims installed)."
echo "================================================================================"
