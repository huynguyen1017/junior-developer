# JUNIOR DEVELOPER v8.0 & ENGR 852 v7.1 — Verification & Security Audit Report

- **Staging Endpoint Tested**: `http://127.0.0.1:8789`
- **v7.1 Fault-Injection & Native Verdi Suite (`T01`–`T25`)**: `25 / 25 PASSED`
- **v8.0 Public Platform & Security Suite (`AC01`–`AC15`)**: `15 / 15 PASSED`

## 1. Junior Developer v8.0 Acceptance Matrix (`AC01`–`AC15`)

| ID | Acceptance / Security Gate | Status | Evidence Class | Verified Detail |
|---|---|---|---|---|
| `AC01` | Public Homepage, RDAP Domain Readiness, Strict CORS & Zero PII/Optimistic Checkmarks | **PASS** | `NATIVE_EXECUTION` | status=200/200, evil_origin_acao='', optimistic_checkmarks=False, pii_leaks=[] |
| `AC02` | Guest Sandbox Provisioning, Student Registration & PBKDF2-HMAC-SHA256 Login | **PASS** | `NATIVE_EXECUTION` | guest_token_len=60, user1=maya_43031 (usr_081510293a9a), login_status=200 |
| `AC03` | Guest-to-Student Migration Preserves Guest Sandbox Projects & Progress | **PASS** | `NATIVE_EXECUTION` | migrated_user=liam_43031 (usr_guest_183a6830c6), preserved_project=proj_c59600a3cd75, fetch_status=200 |
| `AC04` | Multi-Tenant 0700 Project Isolation, Cross-User 403 & Spoofed user_id 403 | **PASS** | `NATIVE_EXECUTION` | u1_proj=proj_f6705b6935de, cross_user_get=403, spoofed_user_id_post=403, unauth_post=401 |
| `AC05` | Open-Source Verilog (iverilog + vvp + Yosys) Real VCD Execution & Unsafe $system Sandbox Block | **PASS** | `NATIVE_EXECUTION` | run_status=PASS, evidence=OPEN_SOURCE_SIMULATION_VERIFIED, vcd_transitions=1263, unsafe_task_http=403 |
| `AC06` | Non-Destructive Project Reset & Historical Archive Preservation | **PASS** | `NATIVE_EXECUTION` | reset_http=200, archive_id=arch_proj_f6705b6935de_1794343032 |
| `AC07` | Junior Connect 8 Communities, Posts, Nested Comments, Voting, Accepted Solution, Save & Moderation | **PASS** | `NATIVE_EXECUTION` | communities=8, post_id=post_d39e52b7f33a, comment_id=cmt_31a8e63349f2, vote/accept/save/report=200/200/200/200 |
| `AC08` | Automatic Privacy & Secret Redaction on Shared Junior Connect Debugging Posts | **PASS** | `NATIVE_EXECUTION` | sanitized_body='My log showed path /workspace/student/project and host <redacted_inst_id>@<private_eda_host> at <redacted_vpn_...' |
| `AC09` | Junior Messenger 1-to-1 DMs, Study Rooms, Reactions & Non-Member Access Block (403) | **PASS** | `NATIVE_EXECUTION` | dm_id=conv_6d8a793df84b, msg_http=200, react_http=200, non_member_read_http=403 |
| `AC10` | Junior Messenger User Block Enforcement (403 on Blocked Sender) | **PASS** | `NATIVE_EXECUTION` | block_http=200, blocked_sender_http=403 |
| `AC11` | Continuous SSE Stream Authentication (401 Unauth), Monotonic id: & Last-Event-ID Replay | **PASS** | `NATIVE_EXECUTION` | unauth_http=401, auth_http=200, has_event_id=True |
| `AC12` | Scoped AI Agent v8 Suite (KnowledgeRetrieval, Community, Conversation, LearningMatch, TrustAndSafety) | **PASS** | `NATIVE_EXECUTION` | mentor_http=200, study_match_http=200 |
| `AC13` | Preserved 100-Page ENGR 852 Studio, Verified Fig 10 Redacted Capture & Fail-Closed 422 on Unredacted Frame | **PASS** | `NATIVE_EXECUTION` | curriculum_pages=100, fig10_frame_http=200, unredacted_failclosed_http=422 |
| `AC14` | Student Account JSON Export & Account Deletion / Anonymization | **PASS** | `NATIVE_EXECUTION` | export_http=200, delete_http=200 |
| `AC15` | Combined v7.1 (25/25) & v8.0 Acceptance Gate | **PASS** | `NATIVE_EXECUTION` | v7_1_passed=25/25, v8_0_prior_passed=14/14 |

## 2. ENGR 852 v7.1 Native Verdi & Fault-Injection Matrix (`T01`–`T25`)

| ID | Scenario | Status | Evidence Class | Detail |
|---|---|---|---|---|
| `T01` | Intentional Shell/Verilog Syntax Error | **PASS** | `FAILED` | Exit=2, Diagnosis=FAULT_SYNTAX_ERROR |
| `T02` | Missing RTL Source File | **PASS** | `FAILED` | Exit=1, Diagnosis=FAULT_MISSING_RTL_OR_FILE |
| `T03` | Failing Hardware Testbench Assertion | **PASS** | `FAILED` | Exit=1, Reason=Process failed with non-zero exit code (1). |
| `T04` | Missing FSDB Waveform Database | **PASS** | `FAILED` | Simulation waveform database not found: /var/folders/xk/mqxkwfj14m5bgj0rm79strs80000gn/T/<REDACTED_TOKEN>/nonexistent_missing_wave.fsdb |
| `T05` | Unavailable Synopsys SCL License | **PASS** | `FAILED` | Synopsys license server unavailable. |
| `T06` | Broken SSH Connectivity to EDA Server | **PASS** | `FAILED` | SSH/X11 connection to EDA server failed. |
| `T07` | Unavailable XQuartz Application | **PASS** | `FAILED` | XQuartz is not installed or unavailable on this Mac. |
| `T08` | Failed Git Push (Unreachable/Rejected Remote) | **PASS** | `FAILED` | Git push failed (exit 128): fatal: unable to access 'https://127.0.0.1:9/nonexistent-invalid-repo.git/': Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server |
| `T09` | Conflicting Changes Across Two Macs (iMac vs MacBook Air) | **PASS** | `FAILED` | MULTI_MAC_DIVERGENCE_DETECTED: Remote branch has commits from another Mac (e.g. iMac @ 4fe81ae vs MacBook Air @ b801452) or local worktree has uncommitted modifications. Refusing blind rebase/force-push; isolate onto per-device branch 'run-imac-1794343018'. |
| `T10` | Cancelled Run Mid-Execution | **PASS** | `FAILED` | Exit=-15, State=CANCELLED |
| `T11` | Immutable Reset + Subsequent Run Preserving Prior History & Failures | **PASS** | `NATIVE_EXECUTION` | OldRun=run_20261110T203256Z_18a0d1 (ARCHIVED), NewRun=run_20261110T203658Z_f979ee (ACTIVE), PriorFailedJob=FAILED |
| `T12` | Unauthorized User / Forged Token Attempting Another User's Actions | **PASS** | `FAILED` | Blocked Reason: Cross-user access denied: token belongs to 'forged_invalid_token', not 'unauthorized_intruder_user' |
| `T13` | Misleading Expected PASS Marker in Failed Command Output (Exit Code != 0) | **PASS** | `FAILED` | Exit=2, MisleadingMarkerDetected=True -> MISLEADING_PASS_MARKER_REJECTED: Process exited with non-zero code (2) despite printing PASS/VERIFIED text in stdout. Independent verifier rejected PASS claim. |
| `T14` | Authentic Synopsys Verdi Process & Novas X11 Window Detection | **PASS** | `REAL_APPLICATION_CAPTURE` | WindowID=0x1400006, Title=<Verdi-Apex:nTraceMain:1> motion_v5_16bit_top_regression_tb motio |
| `T15` | Non-Empty FSDB Verification via fsdb2vcd (200 Variables & Required Signal Paths) | **PASS** | `NATIVE_EXECUTION` | FSDB=motion_v5_16bit_top_regression.fsdb (252336 bytes, 200 vars, matched=17/17 signals) |
| `T16` | Successful Tcl Replay & Non-Zero Signal-Rail Verification (Rejects Empty G1 Panel) | **PASS** | `REAL_APPLICATION_CAPTURE` | RailBands=22, GreenScanlines=142, EmptyG1Rejected=GUI_OPEN_SIGNAL_VERIFICATION_PENDING |
| `T17` | Waveform Data, Cursor Positioning (count=0x0100) & Interactive Teaching Actions | **PASS** | `REAL_APPLICATION_CAPTURE` | Actions=[highlight_bestdist, jump_count_0x0100, explain_motionx_change], AnnotatedSHA=b2a30333e51e |
| `T18` | Incorrect GUI Window Selection Rejection (Non-Novas XTerm Window) | **PASS** | `FAILED` | Window verifier rejected non-Novas X11 window (WM_CLASS='XTerm'). |
| `T19` | Failed or Missing Screenshot Rejection | **PASS** | `FAILED` | Application-only screenshot capture missing or invalid. |
| `T20` | Privacy & Path Redaction Verification on Window-Only Captures (0600 Mode & Multi-Zone Redaction) | **PASS** | `REAL_APPLICATION_CAPTURE` | Redacted=True, Verified=True, Mode=0600, RedactedSHA=723ae2736a462d |
| `T21` | Educational Demo (EDUCATIONAL_SIMULATION) vs. Native Execution Classification | **PASS** | `EDUCATIONAL_SIMULATION` | SimClass=EDUCATIONAL_SIMULATION vs NativeClass=REAL_APPLICATION_CAPTURE |
| `T22` | Service Restart & Interrupted Job Crash Recovery | **PASS** | `FAILED` | Stale RUNNING job job_stale_7d8b5210 transitioned to FAILED (recovered_after_restart=True) |
| `T23` | Two Concurrent Users Executing Simultaneously Without Workspace Collisions | **PASS** | `NATIVE_EXECUTION` | AlphaDir=attempt_003_job_63b4ac48cc79, BetaDir=attempt_003_job_afd447d7fe04 |
| `T24` | Non-Destructive Reset Preserving All 100 Tracked Git Logs & 100 PNGs | **PASS** | `NATIVE_EXECUTION` | Tracked logs=100, Tracked screenshots=100 (0 deleted) |
| `T25` | V9 ASIC Sign-Off Technical Integrity & Waiver Disclosure Audit | **PASS** | `DERIVED_ANALYSIS` | Disclosed gaps=['GAP-01', 'GAP-02', 'GAP-03', 'GAP-04', 'GAP-05'] (PrimeTime coverage, SLOW max/min_cap, FC check_lvs vs standalone LVS) |
