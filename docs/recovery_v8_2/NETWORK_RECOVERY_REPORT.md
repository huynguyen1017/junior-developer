# JUNIOR DEVELOPER v8.2 — Network & Transport Recovery Report

## 1. Layered Network Diagnostic Chain

The `NetworkHealthAgent` (`GET /api/v8/network/health` and `run_network_and_eda_preflight()`) evaluates connectivity in strict causal order without modifying system network routes or killing the user's GlobalProtect VPN client:

1. **Layer 1 — Local Website Host (`127.0.0.1:8789`)**: Verified active under `launchd` (`com.juniordeveloper.engr852.staging8789.plist`), completely isolated from Production (`127.0.0.1:8788`, PID `46103`).
2. **Layer 2 — SFSU GlobalProtect VPN Interface (`utun*`)**: Inspects active `utun` interfaces and routing table entries (`route -n get <private_eda_host>`) to distinguish `VPN_CLIENT_NOT_RUNNING` from `VPN_ROUTE_UNAVAILABLE`.
3. **Layer 3 — DNS Resolution (`socket.getaddrinfo`)**: Verifies resolution of `<private_eda_host>` port `22`.
4. **Layer 4 — SSH TCP Transport (`socket.create_connection`, 3.0s timeout)**: Distinguishes `SSH_TCP_TIMEOUT` (campus TCP `:22` firewall/tunnel idle drop while GlobalProtect GUI still displays "Connected") from `SSH_AUTH_FAILED`.
5. **Layer 5 — Non-Interactive SSH Authentication (`ssh -F ~/.ssh/config -o BatchMode=yes`)**: Uses explicit `-F ~/.ssh/config` so `launchd`/non-interactive shells always resolve the owner's SSH key and host alias.
6. **Layer 6 — Local XQuartz Display (`xset q` & `DISPLAY` socket)**: Verifies local X11 reachability before attempting remote `ssh -Y` forwarding.

## 2. Circuit Breaker & Exponential Backoff

- **State File**: `practice_from_scratch/web_console/state_store/network_health/latest.json` (permissions `0600`).
- **Backoff Schedule**: `10s -> 20s -> 40s -> 60s` on consecutive transport failures (`SSH_TCP_TIMEOUT` or `VPN_ROUTE_UNAVAILABLE`), preventing cascading SSH subprocess storms while allowing instant manual override via `?force=1` or the **Reconnect & Verify SSH/Verdi** button.
