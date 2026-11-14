#!/usr/bin/env python3
"""Read-only bounded SSH/VPN/XQuartz diagnosis for JUNIOR DEVELOPER staging.

NO automatic VPN changes, credential reads in logs, process termination, or GUI relaunch.
Records only redacted network state; designed for a privileged owner-companion worker.
"""
import argparse
import datetime as dt
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time

ROOT = Path.home() / "Developer/ENGR852_Stability_Recovery_20261111"
STATE_FILE = ROOT / "network_health" / "latest.json"


def classify(dns_ok, tcp_ok, xquartz_ok, ssh_auth=None):
    if not dns_ok:
        return "DNS_RESOLUTION_FAILED", "Inspect DNS and VPN resolver configuration"
    if not tcp_ok:
        return "SSH_TCP_TIMEOUT", "Preserve GUI/evidence; retry TCP with bounded backoff; ask the user to verify authorized campus VPN or server reachability"
    if ssh_auth is False:
        return "SSH_AUTHENTICATION_REQUIRED", "Request owner-companion reauthorization; never bypass university controls"
    if not xquartz_ok:
        return "XQUARTZ_UNAVAILABLE", "Request permission to open XQuartz on the authorized desktop"
    if ssh_auth is True:
        return "SSH_X11_PREFLIGHT_READY", "Attach to an existing matching Verdi window or launch only with authorization"
    return "SSH_TRANSPORT_READY", "Check SSH authorization and X11 before launching native tools"


def run_checked(args, timeout=4):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None


def probe_once():
    # University host is read locally, never logged or transmitted as a raw identifier.
    sys.path.insert(0, str(Path.home() / "Developer/portfolio/motion-estimator-v7-native-verdi-staged/practice_from_scratch/scripts"))
    try:
        import engr852_native_verdi_bridge as bridge
        cfg = bridge._load_owner_private_config()
        host = cfg.get("eda_server_host") or str(bridge.REMOTE).rsplit("@", 1)[-1]
    except Exception:
        host = ""
    result = {
        "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "schema": "ENGR852_CONNECTION_HEALTH_V1",
        "network_host_redacted": True,
        "host_fingerprint": hashlib.sha256(host.encode()).hexdigest()[:12] if host else None,
        "configured_host": bool(host),
        "dns_resolved": False,
        "ssh_tcp_connected": False,
        "route_interface": "UNKNOWN",
        "xquartz_ready": False,
        "vpn_process_seen": False,
        "window_count": 0,
    }
    vpn = run_checked(["pgrep", "-fl", "GlobalProtect|PanGPS"], timeout=2)
    result["vpn_process_seen"] = bool(vpn and vpn.returncode == 0 and vpn.stdout.strip())
    disp = os.environ.get("DISPLAY", "")
    if not disp:
        la = run_checked(["launchctl", "getenv", "DISPLAY"])
        disp = (la.stdout or "").strip() if la and la.returncode == 0 else ""
    if disp and Path("/opt/X11/bin/xset").is_file():
        try:
            s = subprocess.run(["/opt/X11/bin/xset", "q"], capture_output=True, timeout=3, env={**os.environ, "DISPLAY": disp})
            result["xquartz_ready"] = s.returncode == 0
        except Exception:
            pass
    try:
        if host:
            ip = socket.getaddrinfo(host, 22, type=socket.SOCK_STREAM)[0][4][0]
            result["dns_resolved"] = True
            result["destination_is_global"] = ipaddress.ip_address(ip).is_global
            route = run_checked(["route", "-n", "get", ip])
            if route:
                m = re.search(r"interface:\s*(\S+)", route.stdout)
                if m:
                    result["route_interface"] = m.group(1)
            try:
                with socket.create_connection((ip, 22), timeout=4):
                    result["ssh_tcp_connected"] = True
            except OSError:
                pass
    except (OSError, ValueError):
        pass
    result["code"], result["recommended_action"] = classify(
        result["dns_resolved"],
        result["ssh_tcp_connected"],
        result["xquartz_ready"],
    )
    result["status"] = "READY_FOR_AUTHENTICATED_SSH" if result["ssh_tcp_connected"] else "BLOCKED"
    result["no_system_mutations"] = True
    return result


def save_result(result):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(STATE_FILE.parent, 0o700)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2), encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, STATE_FILE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=1, help="bounded number of diagnostic samples, max 10")
    args = ap.parse_args()
    samples = max(1, min(10, args.samples))
    for i in range(samples):
        result = probe_once()
        result["sample_index"] = i + 1
        save_result(result)
        print(json.dumps(result, sort_keys=True), flush=True)
        if result["ssh_tcp_connected"]:
            break
        if i + 1 < samples:
            time.sleep(min(60, 5 * (2 ** i)))


if __name__ == "__main__":
    main()
