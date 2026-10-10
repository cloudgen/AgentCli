# =============================================================================
# tests/test_cli.sh — CLI surface (no public network; off-TTY empty argv is Type O already-installed)
# =============================================================================
# Primary REQs: requirement-shell-cli-interface, requirement-shell-cli-zero-arguments,
# requirement-shell-cli-default-interaction, requirement-shell-output-requirements,
# requirement-shell-cli-storage, requirement-shell-internal-volatile-timer
# TP family: TP-CLI-*
# =============================================================================

# shellcheck source=helpers.sh
. "${TESTS_ROOT}/helpers.sh"

run_test_cli() {
    t_header "CLI surface (TP-CLI)"

    require_cmd sh
    require_cmd grep
    # TP-CLI-01 syntax
    sh -n "${SCRIPT}"
    assert_eq "TP-CLI-01 sh -n ship unit" 0 "$?"

    # TP-CLI-15 / TP-ELEV-10: no command-substitution of read helpers
    _src=$(cat "${SCRIPT}")
    assert_not_contains "TP-CLI-15 no \$(prompt_ask" "${_src}" '$(prompt_ask'
    assert_not_contains "TP-CLI-15 no \$(prompt_yes_no" "${_src}" '$(prompt_yes_no'

    # TP-CLI-02 version human
    _out=$(sh "${SCRIPT}" version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-02 version exit 0" 0 "$_ec"
    assert_contains "TP-CLI-02 version mentions app" "$_out" "${APP_NAME}"
    assert_contains "TP-CLI-02 version mentions VERSION" "$_out" "${PRODUCT_VERSION}"

    # TP-CLI-03 version json
    _out=$(sh "${SCRIPT}" --json version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-03 version --json exit 0" 0 "$_ec"
    assert_contains "TP-CLI-03 type version" "$_out" '"type":"version"'
    assert_contains "TP-CLI-03 app field" "$_out" "\"app\":\"${APP_NAME}\""
    assert_contains "TP-CLI-03 version field" "$_out" "\"version\":\"${PRODUCT_VERSION}\""

    # TP-CLI-04 help lists local lifecycle + domain; not online verbs
    _out=$(sh "${SCRIPT}" help 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-04 help exit 0" 0 "$_ec"
    assert_contains "TP-CLI-04 help install" "$_out" "install"
    assert_contains "TP-CLI-04 help setup" "$_out" "setup"
    assert_contains "TP-CLI-04 help update-grok" "$_out" "update-grok"
    assert_contains "TP-CLI-04 help reinstall" "$_out" "reinstall"
    assert_contains "TP-CLI-04 help run" "$_out" "run"
    assert_contains "TP-CLI-04 help menu" "$_out" "menu"
    assert_contains "TP-CLI-04 help uninstall" "$_out" "uninstall"
    assert_contains "TP-CLI-04 help where-is-me" "$_out" "where-is-me"
    assert_contains "TP-CLI-04 help backup" "$_out" "backup"
    assert_contains "TP-CLI-04 help check-session" "$_out" "check-session"
    assert_contains "TP-CLI-04 help sync-auth" "$_out" "sync-auth"
    assert_contains "TP-CLI-04 help sync-auth-from-remote" "$_out" "sync-auth-from-remote"
    assert_contains "TP-CLI-04 help sync-auth-to-remote" "$_out" "sync-auth-to-remote"
    assert_contains "TP-CLI-04 help add-crontab" "$_out" "add-crontab"
    assert_not_contains "TP-CLI-04 help no restore" "$_out" "restore <"
    assert_contains "TP-CLI-04 help print-sudoers" "$_out" "print-sudoers"
    assert_contains "TP-CLI-04 help install-script" "$_out" "print-sudoers-install-script"
    assert_contains "TP-CLI-04 help remove-project-sudoers" "$_out" "remove-project-sudoers"
    assert_contains "TP-CLI-04 help submit-sudoer-request" "$_out" "submit-sudoer-request"
    assert_contains "TP-CLI-04 help generate-sudoer-request" "$_out" "generate-sudoer-request"
    assert_contains "TP-CLI-04 help public inbound" "$_out" "/var/sudoer-cli/sudoer-request"
    assert_contains "TP-CLI-04 help --update" "$_out" "--update"
    assert_contains "TP-CLI-04 help --add" "$_out" "--add"
    assert_contains "TP-CLI-04 help SUDOER_PUBLIC_ROOT" "$_out" "SUDOER_PUBLIC_ROOT"
    assert_contains "TP-CLI-04 help GROK_CLI_ROOT" "$_out" "GROK_CLI_ROOT"
    assert_contains "TP-CLI-04 help --json" "$_out" "--json"
    assert_contains "TP-CLI-04 help --debug" "$_out" "--debug"
    assert_contains "TP-CLI-04 help --debug elapsed" "$_out" "elapsed of each paint step"
    assert_contains "TP-CLI-04 help self-update" "$_out" "self-update"
    assert_contains "TP-CLI-04 help self-uninstall" "$_out" "self-uninstall"
    assert_contains "TP-CLI-04 help version-check" "$_out" "version-check"
    assert_contains "TP-CLI-04 help SCRIPT_URL channel" "$_out" "SCRIPT_URL"
    assert_contains "TP-CLI-04 help testers heading" "$_out" "Test-purpose"
    assert_contains "TP-CLI-04 help rc-test" "$_out" "rc-test"
    assert_contains "TP-CLI-04 help BASHRC env" "$_out" "BASHRC"
    assert_contains "TP-CLI-04 help ZSHENV env" "$_out" "ZSHENV"
    assert_not_contains "TP-CLI-04 no CHECKSUM" "$_out" "CHECKSUM"

    # TP-CLI-05 help json
    _out=$(sh "${SCRIPT}" --json help 2>/dev/null)
    assert_eq "TP-CLI-05 help --json exit 0" 0 "$?"
    assert_contains "TP-CLI-05 help json success" "$_out" '"type":"success"'

    # TP-CLI-06 about json domain + cache folders, no channel
    # Isolate PATH so about's session probe cannot call a host grok (xAI).
    ci_isolated_env
    _out=$(HOME="${CI_HOME}" sh "${SCRIPT}" --json about 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-06 about --json exit 0" 0 "$_ec"
    assert_contains "TP-CLI-06 type about" "$_out" '"type":"about"'
    assert_contains "TP-CLI-06 cache_used" "$_out" '"cache_used"'
    assert_contains "TP-CLI-06 cache_preferred" "$_out" '"cache_preferred"'
    assert_contains "TP-CLI-06 cache_fallback" "$_out" '"cache_fallback"'
    assert_contains "TP-CLI-06 cache_fallback_2" "$_out" '"cache_fallback_2"'
    assert_contains "TP-CLI-06 persistence_storage" "$_out" '"persistence_storage"'
    assert_contains "TP-CLI-06 effective_storage" "$_out" '"effective_storage"'
    _hum=$(HOME="${CI_HOME}" sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-06 human Cache folder used" "$_hum" "Cache folder used:"
    assert_contains "TP-CLI-06 human Cache folder preferred" "$_hum" "Cache folder (preferred):"
    assert_contains "TP-CLI-06 human Cache folder 1st fallback" "$_hum" "Cache folder (1st fallback):"
    assert_contains "TP-CLI-06 human Cache folder 2nd fallback" "$_hum" "Cache folder (2nd fallback):"
    assert_contains "TP-CLI-06 human Persistence storage" "$_hum" "Persistence storage:"
    assert_not_contains "TP-CLI-06 no Storage (effective) label" "$_hum" "Storage (effective)"
    assert_not_contains "TP-CLI-06 no Storage (fallback) label" "$_hum" "Storage (fallback)"
    assert_contains "TP-CLI-06 grok_cli_root" "$_out" '"grok_cli_root"'
    assert_contains "TP-CLI-06 deposit_dir" "$_out" '"deposit_dir"'
    assert_contains "TP-CLI-06 session" "$_out" '"session"'
    assert_contains "TP-CLI-06 sudoer_cli" "$_out" '"sudoer_cli"'
    assert_contains "TP-CLI-06 sudoer_adm" "$_out" '"sudoer_adm"'
    assert_contains "TP-CLI-06 sudoer_inbound" "$_out" '"sudoer_inbound"'
    assert_contains "TP-CLI-06 host_sudoers_present" "$_out" '"host_sudoers_present"'
    assert_not_contains "TP-CLI-06 no CHECKSUM" "$_out" "CHECKSUM"
    assert_not_contains "TP-CLI-06 no SCRIPT_URL" "$_out" "SCRIPT_URL"
    ci_cleanup_env

    # TP-CLI-07 empty argv: off-TTY Type O ensure (not help). TTY: numbered menu.
    ci_isolated_env
    HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" install >/dev/null 2>&1
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-07 empty argv off-TTY exit 0" 0 "$_ec"
    assert_contains "TP-CLI-07 empty argv off-TTY already installed" "$_out" "already installed"
    assert_not_contains "TP-CLI-07 empty argv off-TTY not help dump" "$_out" "Usage:"
    assert_not_contains "TP-CLI-07 empty argv off-TTY not numbered list" "$_out" "9. Exit"
    ci_cleanup_env

    _out=$(sh "${SCRIPT}" --json 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-07 --json no command exit 0" 0 "$_ec"
    assert_contains "TP-CLI-07 --json no command is JSON help" "$_out" '"type":"success"'
    assert_not_contains "TP-CLI-07 --json no command not numbered list" "$_out" "9. Exit"

    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="9" ci_pty_capture "${SCRIPT}")
        assert_contains "TP-CLI-07 TTY empty argv is numbered list" "$_out" "9. Exit"
        assert_contains "TP-CLI-07 TTY empty argv grok-auth first" "$_out" "1. grok-auth:"
        assert_not_contains "TP-CLI-07 TTY empty argv no check-session row" "$_out" "check-session:"
        assert_contains "TP-CLI-07 TTY empty argv header app" "$_out" "${APP_NAME}"
        assert_contains "TP-CLI-07 TTY empty argv header version" "$_out" "${PRODUCT_VERSION}"
        assert_not_contains "TP-CLI-07 TTY empty argv not help dump" "$_out" "Usage:"
        _jout=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="9" ci_pty_capture "${SCRIPT}" --json)
        assert_contains "TP-CLI-07 TTY --json no command is JSON help" "$_jout" '"type":"success"'
        assert_not_contains "TP-CLI-07 TTY --json no command not numbered list" "$_jout" "9. Exit"
        assert_not_contains "TP-CLI-07 TTY --json no command not menu dispatch" "$_jout" "command=menu"
        unset _jout
        ci_cleanup_env
    else
        t_skip "TP-CLI-07 TTY empty argv (no python3 for PTY)"
        t_skip "TP-CLI-07 TTY --json no command (no python3 for PTY)"
    fi

    # TP-CLI-29 overlay flags-only follow empty argv; --json stays JSON help.
    ci_isolated_env
    HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" install >/dev/null 2>&1
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" --debug 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-29 --debug no command off-TTY exit 0" 0 "$_ec"
    assert_contains "TP-CLI-29 --debug no command off-TTY ensure" "$_out" "already installed"
    assert_not_contains "TP-CLI-29 --debug no command off-TTY not help dump" "$_out" "Usage:"
    assert_not_contains "TP-CLI-29 --debug no command off-TTY not numbered list" "$_out" "9. Exit"
    _err=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" --debug 2>&1 >/dev/null)
    assert_contains "TP-CLI-29 --debug no command off-TTY debug tag" "$_err" "[DEBUG]"
    assert_contains "TP-CLI-29 --debug no command off-TTY dispatch ensure" "$_err" "command=ensure"
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" --quiet 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-29 --quiet no command off-TTY exit 0" 0 "$_ec"
    assert_not_contains "TP-CLI-29 --quiet no command off-TTY not help dump" "$_out" "Usage:"
    assert_not_contains "TP-CLI-29 --quiet no command off-TTY not numbered list" "$_out" "9. Exit"
    _out=$(sh "${SCRIPT}" --json --debug 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-29 --json --debug no command exit 0" 0 "$_ec"
    assert_contains "TP-CLI-29 --json --debug no command is JSON help" "$_out" '"type":"success"'
    assert_not_contains "TP-CLI-29 --json --debug no command not numbered list" "$_out" "9. Exit"
    ci_cleanup_env

    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="9" ci_pty_capture "${SCRIPT}" --debug)
        assert_contains "TP-CLI-29 TTY --debug no command is numbered list" "$_out" "9. Exit"
        assert_contains "TP-CLI-29 TTY --debug no command grok-auth first" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-29 TTY --debug no command dispatch menu" "$_out" "command=menu"
        assert_contains "TP-CLI-29 TTY --debug no command paint start" "$_out" "menu step paint: start"
        assert_not_contains "TP-CLI-29 TTY --debug no command not help dump" "$_out" "Usage:"
        ci_cleanup_env
    else
        t_skip "TP-CLI-29 TTY --debug no command (no python3 for PTY)"
    fi

    # TP-CLI-08 unknown command fail-closed
    _err=$(sh "${SCRIPT}" no-such-command 2>&1 >/dev/null)
    _ec=$?
    assert_eq "TP-CLI-08 unknown exit 1" 1 "$_ec"
    assert_contains "TP-CLI-08 unknown error text" "$_err" "Unknown command"

    _err=$(sh "${SCRIPT}" --json no-such-command 2>&1 >/dev/null)
    _ec=$?
    assert_eq "TP-CLI-08 unknown --json exit 1" 1 "$_ec"
    assert_contains "TP-CLI-08 unknown --json type" "$_err" '"type":"out_error"'

    # TP-CLI-09 quiet suppresses version info
    _out=$(sh "${SCRIPT}" --quiet version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-09 quiet version exit 0" 0 "$_ec"
    _trim=$(printf '%s' "$_out" | tr -d ' \t\n\r')
    if [ -z "$_trim" ]; then
        t_pass "TP-CLI-09 quiet suppresses human version"
    else
        t_fail "TP-CLI-09 quiet expected empty stdout, got '$(_trunc "$_out")'"
    fi

    # TP-CLI-10 online verbs are routed (refuse URL; never hang on GitHub).
    _err=$(SCRIPT_URL="http://127.0.0.1:1/grok-cli" timeout 8 \
        sh "${SCRIPT}" self-update 2>&1 >/dev/null) || true
    assert_not_contains "TP-CLI-10 self-update is routed" "${_err}" "Unknown command"
    _err=$(SCRIPT_URL="http://127.0.0.1:1/grok-cli" timeout 8 \
        sh "${SCRIPT}" version-check 2>&1 >/dev/null) || true
    assert_not_contains "TP-CLI-10 version-check is routed" "${_err}" "Unknown command"

    # TP-CLI-11 set -u HOME unset still works for version
    _out=$(env -u HOME sh "${SCRIPT}" version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-11 env -u HOME version exit 0" 0 "$_ec"
    assert_contains "TP-CLI-11 env -u HOME version text" "$_out" "${PRODUCT_VERSION}"

    # TP-CLI-12 cache isolation under temp HOME (per login + process id)
    ci_isolated_env
    _login=$(id -un 2>/dev/null || echo "unknown")
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" --json about 2>/dev/null)
    assert_contains "TP-CLI-12 isolated about has app in cache" "$_out" "${APP_NAME}"
    _pref=$(printf '%s' "$_out" | sed -n 's/.*"cache_preferred":"\([^"]*\)".*/\1/p' | head -n1)
    _pid="${_pref##*-}"
    case "${_pref}" in
        /dev/shm/cache/cache-"${APP_NAME}"-"${_login}"-[0-9]*)
            t_pass "TP-CLI-12 cache_preferred is shm login process leaf"
            ;;
        *) t_fail "TP-CLI-12 cache_preferred unexpected: '${_pref:-empty}'" ;;
    esac
    _fb=$(printf '%s' "$_out" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 cache_fallback 1st" "/tmp/cache/cache-${APP_NAME}-${_login}-${_pid}" "${_fb}"
    _fb2=$(printf '%s' "$_out" | sed -n 's/.*"cache_fallback_2":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 cache_fallback 2nd" "${CI_HOME}/.cache/cache-${APP_NAME}-${_pid}" "${_fb2}"
    _used=$(printf '%s' "$_out" | sed -n 's/.*"cache_used":"\([^"]*\)".*/\1/p' | head -n1)
    _eff=$(printf '%s' "$_out" | sed -n 's/.*"effective_storage":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 cache_used matches effective" "${_eff}" "${_used}"
    if [ -n "$_eff" ] && [ -d "$_eff" ]; then
        t_pass "TP-CLI-12 effective cache directory exists"
    else
        t_fail "TP-CLI-12 effective cache missing: '${_eff:-empty}'"
    fi
    case "${_eff}" in
        /dev/shm/"${APP_NAME}"|/dev/shm/"${APP_NAME}"-*)
            t_fail "TP-CLI-12 effective cache must not be ram-drive project shape: '${_eff}'"
            ;;
        *) t_pass "TP-CLI-12 effective cache is not a ram-drive project shape" ;;
    esac
    _err=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GROK_CLI_CACHE_SKIP=preferred \
        sh "${SCRIPT}" about 2>&1 >/dev/null)
    assert_not_contains "TP-CLI-12 silent cache fallback" "${_err}" "fallback"
    assert_not_contains "TP-CLI-12 silent cache fallback error" "${_err}" "Cannot create cache"
    _skip=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GROK_CLI_CACHE_SKIP=preferred \
        sh "${SCRIPT}" --json about 2>/dev/null)
    _skip_eff=$(printf '%s' "$_skip" | sed -n 's/.*"effective_storage":"\([^"]*\)".*/\1/p' | head -n1)
    _skip_fb=$(printf '%s' "$_skip" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 skipped preferred uses 1st fallback" "${_skip_fb}" "${_skip_eff}"
    _gb=$(HOME="${CI_HOME}" GROK_CLI_CACHE_HOST=gitbash sh "${SCRIPT}" --json about 2>/dev/null)
    _gb_pref=$(printf '%s' "$_gb" | sed -n 's/.*"cache_preferred":"\([^"]*\)".*/\1/p' | head -n1)
    _gb_pid="${_gb_pref##*-}"
    assert_eq "TP-CLI-12 gitbash preferred" "/tmp/cache/cache-${APP_NAME}-${_login}-${_gb_pid}" "${_gb_pref}"
    _gb_fb=$(printf '%s' "$_gb" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 gitbash 1st fallback" "${CI_HOME}/AppData/Local/Temp/cache-${APP_NAME}-${_gb_pid}" "${_gb_fb}"
    assert_contains "TP-CLI-12 gitbash json has cache_fallback_2" "${_gb}" '"cache_fallback_2":""'
    _gb_fb2=$(printf '%s' "$_gb" | sed -n 's/.*"cache_fallback_2":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 gitbash no 2nd fallback" "" "${_gb_fb2}"
    _mac=$(HOME="${CI_HOME}" GROK_CLI_CACHE_HOST=mac sh "${SCRIPT}" --json about 2>/dev/null)
    _mac_pref=$(printf '%s' "$_mac" | sed -n 's/.*"cache_preferred":"\([^"]*\)".*/\1/p' | head -n1)
    _mac_pid="${_mac_pref##*-}"
    assert_eq "TP-CLI-12 mac preferred" "/tmp/cache/cache-${APP_NAME}-${_login}-${_mac_pid}" "${_mac_pref}"
    _mac_fb=$(printf '%s' "$_mac" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 mac 1st fallback" "${CI_HOME}/Library/Caches/cache-${APP_NAME}-${_mac_pid}" "${_mac_fb}"
    _mac_fb2=$(printf '%s' "$_mac" | sed -n 's/.*"cache_fallback_2":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 mac 2nd fallback" "${CI_HOME}/cache/cache-${APP_NAME}-${_mac_pid}" "${_mac_fb2}"
    _mode=$(stat -c %a "${_eff}" 2>/dev/null || echo "")
    assert_eq "TP-CLI-12 effective cache mode 0700" "700" "${_mode}"
    _hum_l=$(HOME="${CI_HOME}" sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-12 linux about used" "${_hum_l}" "Cache folder used:"
    assert_contains "TP-CLI-12 linux about preferred path" "${_hum_l}" "/dev/shm/cache/cache-${APP_NAME}-${_login}-"
    assert_contains "TP-CLI-12 linux about 2nd path" "${_hum_l}" "/.cache/cache-${APP_NAME}-"
    _hum_gb=$(HOME="${CI_HOME}" GROK_CLI_CACHE_HOST=gitbash sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-12 gitbash about 1st" "${_hum_gb}" "AppData/Local/Temp/cache-${APP_NAME}-"
    assert_not_contains "TP-CLI-12 gitbash about omits 2nd" "${_hum_gb}" "Cache folder (2nd fallback)"
    _hum_mac=$(HOME="${CI_HOME}" GROK_CLI_CACHE_HOST=mac sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-12 mac about 1st" "${_hum_mac}" "Library/Caches/cache-${APP_NAME}-"
    assert_contains "TP-CLI-12 mac about 2nd path" "${_hum_mac}" "Cache folder (2nd fallback): ${CI_HOME}/cache/cache-${APP_NAME}-"
    _persist=$(printf '%s' "$_out" | sed -n 's/.*"persistence_storage":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 persistence_storage path" "${CI_HOME}/.local/${APP_NAME}" "$_persist"
    if [ -n "$_persist" ] && [ -d "$_persist" ]; then
        t_pass "TP-CLI-12 persistence storage directory exists"
    else
        t_fail "TP-CLI-12 persistence storage missing: '${_persist:-empty}'"
    fi
    case "${_persist}" in
        */.local/bin|*/.local/bin/) t_fail "TP-CLI-12 persistence must not be USER_BIN: '${_persist}'" ;;
        *) t_pass "TP-CLI-12 persistence is not the install bin directory" ;;
    esac
    ci_cleanup_env

    # TP-CLI-13 menu/main: off-TTY help; TTY numbered list; empty argv off-TTY is Type O (not help)
    _out=$(sh "${SCRIPT}" menu 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-13 menu off-TTY exit 0" 0 "$_ec"
    assert_contains "TP-CLI-13 menu off-TTY is help" "$_out" "Usage:"
    assert_not_contains "TP-CLI-13 menu off-TTY not the numbered list" "$_out" "9. Exit"

    _out=$(sh "${SCRIPT}" main 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-13 main off-TTY exit 0" 0 "$_ec"
    assert_contains "TP-CLI-13 main off-TTY is help" "$_out" "Usage:"

    _out=$(sh "${SCRIPT}" --json menu 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-13 menu --json off-TTY exit 0" 0 "$_ec"
    assert_contains "TP-CLI-13 menu --json off-TTY JSON help" "$_out" '"type":"success"'
    assert_not_contains "TP-CLI-13 menu --json off-TTY not numbered list" "$_out" "9. Exit"

    ci_isolated_env
    HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" install >/dev/null 2>&1
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" 2>/dev/null)
    assert_not_contains "TP-CLI-13 empty argv off-TTY not numbered list" "$_out" "9. Exit"
    assert_not_contains "TP-CLI-13 empty argv off-TTY not help" "$_out" "Usage:"
    assert_contains "TP-CLI-13 empty argv off-TTY is ensure" "$_out" "already installed"
    ci_cleanup_env

    _out=$(sh "${SCRIPT}" --quiet menu 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-13 menu --quiet off-TTY exit 0" 0 "$_ec"
    assert_contains "TP-CLI-13 menu --quiet off-TTY still help" "$_out" "Usage:"

    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="99" ci_pty_capture "${SCRIPT}" menu)
        assert_not_contains "TP-CLI-13 TTY menu no check-session row" "$_out" "check-session:"
        assert_contains "TP-CLI-13 TTY menu grok-auth first" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-13 TTY menu language is 5" "$_out" "5. language:"
        assert_not_contains "TP-CLI-13 TTY menu has no row 6 language" "$_out" "6. language:"
        assert_contains "TP-CLI-13 TTY menu sudoers is 8" "$_out" "7. sudoers:"
        assert_contains "TP-CLI-13 TTY menu self-management is 9" "$_out" "8. self-management:"
        assert_not_contains "TP-CLI-13 TTY top hides auth rows" "$_out" "11. backup:"
        assert_contains "TP-CLI-13 TTY menu Exit 0" "$_out" "9. Exit"
        assert_not_contains "TP-CLI-13 TTY top has no Back" "$_out" "0. Back"
        assert_contains "TP-CLI-13 TTY menu header app" "$_out" "${APP_NAME}"
        assert_contains "TP-CLI-13 TTY menu header version" "$_out" "${PRODUCT_VERSION}"
        assert_contains "TP-CLI-13 TTY menu session line" "$_out" "logged out"
        assert_contains "TP-CLI-13 TTY logged-out not-available" "$_out" \
            "backup features are not available for logged-out environment."
        _lo=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'logged-out environment' | head -n1)
        assert_contains "TP-CLI-13 TTY logged-out not-available is INFO" "${_lo}" "[INFO]"
        assert_not_contains "TP-CLI-13 TTY menu no install row" "$_out" "1. Install"
        assert_not_contains "TP-CLI-13 TTY menu no setup row" "$_out" "setup:"
        assert_not_contains "TP-CLI-13 TTY menu no help verb row" "$_out" "help: Show this help"
        assert_not_contains "TP-CLI-13 TTY main hides generate row" "$_out" "1. generate-sudoer-request:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="99" ci_pty_capture "${SCRIPT}" --json menu)
        assert_contains "TP-CLI-13 TTY menu --json still numbered list" "$_out" "9. Exit"
        assert_not_contains "TP-CLI-13 TTY menu --json ignores JSON help" "$_out" '"type":"success"'
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="1
0" ci_pty_capture "${SCRIPT}" menu)
        assert_not_contains "TP-CLI-13 auth hides backup when logged out" "$_out" "11. backup:"
        assert_not_contains "TP-CLI-13 auth sync-auth is not 11" "$_out" "11. sync-auth:"
        assert_contains "TP-CLI-13 auth sync-auth is 13 when logged out" "$_out" "13. sync-auth:"
        assert_not_contains "TP-CLI-13 auth has no row 17" "$_out" "17. sync-auth:"
        assert_contains "TP-CLI-13 auth logged-out not-available" "$_out" \
            "backup features are not available for logged-out environment."
        assert_contains "TP-CLI-13 auth from-remote is 12" "$_out" "12. sync-auth-from-remote:"
        assert_not_contains "TP-CLI-13 auth hides to-remote when logged out" "$_out" \
            "sync-auth-to-remote:"
        assert_contains "TP-CLI-13 auth add-crontab is 14" "$_out" "14. add-crontab:"
        assert_contains "TP-CLI-13 auth setup is 15" "$_out" "15. setup:"
        assert_contains "TP-CLI-13 auth reinstall is 16" "$_out" "16. reinstall:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            GROK_CLI_ROOT="${CI_HOME}/no-global-store" PTY_IN="1
13" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-13 logged-out pick 13 runs sync-auth" "$_out" \
            "Cannot sync-auth: store missing"
        assert_not_contains "TP-CLI-13 logged-out pick 13 is a menu choice" "$_out" \
            "Not a menu choice"
        assert_not_contains "TP-CLI-13 logged-out pick 13 does not backup" "$_out" \
            "Session valid"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="1
11
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-13 logged-out pick 11 is not a menu choice" "$_out" \
            "Not a menu choice"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="1
17
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-13 logged-out pick 17 is not a menu choice" "$_out" \
            "Not a menu choice"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="12
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-13 TTY pick 12 not a menu choice" "$_out" "Not a menu choice"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="0
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-13 TTY top 0 is not a choice" "$_out" "Not a menu choice '0'"
        _nchoice=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c 'Choice:' || true)
        assert_eq "TP-CLI-13 TTY top 0 reprints" "2" "${_nchoice}"
        _nback=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c '0. Back' || true)
        assert_eq "TP-CLI-13 TTY top 0 prints no Back row" "0" "${_nback}"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="7
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-13 TTY submenu generate row" "$_out" "1. generate-sudoer-request:"
        assert_contains "TP-CLI-13 TTY submenu Back 0" "$_out" "0. Back"
        assert_contains "TP-CLI-13 TTY submenu Exit 9" "$_out" "9. Exit"
        _err=$(sh "${SCRIPT}" sudoers 2>&1 >/dev/null)
        assert_eq "TP-CLI-13 sudoers not a live command" 1 "$?"
        assert_contains "TP-CLI-13 sudoers unknown" "$_err" "Unknown command"
        ci_cleanup_env
    else
        t_skip "TP-CLI-13 TTY menu (no python3 for PTY)"
        t_skip "TP-CLI-13 TTY menu --json (no python3 for PTY)"
        t_skip "TP-CLI-13 TTY pick 12 (no python3 for PTY)"
        t_skip "TP-CLI-13 TTY sudoers submenu (no python3 for PTY)"
    fi

    # TP-CLI-17: default CLI main menu style (header nametag; explain SGR 3+37)
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" APP_VERSION="9.9.9" PTY_IN="1
0" ci_pty_capture "${SCRIPT}" menu)
        _bold=$(printf '\033[1m%s\033[0m' "${APP_NAME}")
        _italic=$(printf '\033[3m%s\033[0m' "${PRODUCT_VERSION}")
        _ident=$(printf '\033[1m%s\033[0m(\033[3m%s\033[0m)' "${APP_NAME}" "${PRODUCT_VERSION}")
        _gray_italic=$(printf '\033[3;37m')
        _sgr90=$(printf '\033[90;3m')
        _sync_desc=$(printf '13. sync-auth: \033[3;37mCopy /var/grok-cli/auth.* into ~/.grok\033[0m')
        _backup_desc=$(printf '11. backup: \033[3;37mPush ~/.grok/auth.* to /var/grok-cli\033[0m')
        assert_contains "TP-CLI-17 TTY header bold APP_NAME" "$_out" "${_bold}"
        assert_contains "TP-CLI-17 TTY header italic APP_VERSION" "$_out" "${_italic}"
        assert_contains "TP-CLI-17 TTY header nametag APP_NAME(APP_VERSION)" "$_out" "${_ident}"
        assert_contains "TP-CLI-17 TTY header short desc" "$_out" "Alternative online installer for xAI grok"
        assert_not_contains "TP-CLI-17 TTY header not generic board title" "$_out" "numbered list of live commands"
        assert_not_contains "TP-CLI-17 TTY nametag ignores inherited APP_VERSION" "$_out" "9.9.9"
        assert_contains "TP-CLI-17 TTY logged out when no session" "$_out" "logged out"
        _sess=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'logged out' | head -n1)
        assert_contains "TP-CLI-17 TTY logged out is INFO" "${_sess}" "[INFO]"
        _lo=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'logged-out environment' | head -n1)
        assert_contains "TP-CLI-17 TTY logged-out not-available is INFO" "${_lo}" "[INFO]"
        assert_not_contains "TP-CLI-17 TTY no check-session row" "$_out" "check-session:"
        assert_contains "TP-CLI-17 TTY number and short-descript unstyled" "$_out" "13. sync-auth: "
        assert_not_contains "TP-CLI-17 TTY logged-out hides backup" "$_out" "11. backup:"
        assert_contains "TP-CLI-17 TTY desc is italic + light gray (SGR 3+37)" "$_out" "${_gray_italic}"
        assert_contains "TP-CLI-17 TTY sync-auth explain is gray italic" "$_out" "${_sync_desc}"
        assert_not_contains "TP-CLI-17 TTY not SGR 90 house look" "$_out" "${_sgr90}"
        _after_header=$(printf '%s\n' "$_out" | grep -A1 "Alternative online installer for xAI grok" | head -n2 | tail -n1)
        assert_contains "TP-CLI-17 TTY session line under header" "${_after_header}" "checking session"
        mkdir -p "${CI_HOME}/.grok"
        cat > "${CI_HOME}/.grok/auth.json" <<'AUTH'
{
  "https://auth.x.ai::test-client": {
    "key": "test-access-token",
    "auth_mode": "oidc",
    "refresh_token": "test-refresh-token",
    "expires_at": "2099-01-01T00:00:00Z"
  }
}
AUTH
        ci_fake_grok_ok
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-17 TTY logged in when session valid" "$_out" "logged in"
        assert_not_contains "TP-CLI-17 TTY logged-in not logged out" "$_out" "logged out"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="1
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-17 TTY logged-in lists backup" "$_out" "11. backup:"
        assert_contains "TP-CLI-17 TTY backup explain is gray italic" "$_out" "${_backup_desc}"
        assert_not_contains "TP-CLI-17 TTY logged-in hides sync-auth row" "$_out" "13. sync-auth:"
        assert_not_contains "TP-CLI-17 TTY logged-in has no to-remote row" "$_out" \
            "sync-auth-to-remote:"
        assert_not_contains "TP-CLI-17 TTY logged-in hides logged-out line" "$_out" \
            "not available for logged-out environment."
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="sudoers
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-17 TTY submenu header nametag" "$_out" "${_ident}"
        assert_contains "TP-CLI-17 TTY submenu title" "$_out" "sudoers (grant and drafts)"
        ci_cleanup_env
    else
        t_skip "TP-CLI-17 TTY header/session (no python3 for PTY)"
        t_skip "TP-CLI-17 TTY logged in (no python3 for PTY)"
        t_skip "TP-CLI-17 TTY submenu header (no python3 for PTY)"
    fi

    # TP-CLI-19: this-login-only hosts hide backup / sync-auth / sudoers and
    # print the not-available line under the session (termux / gitbash / windows-cmd).
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-19 Termux not-available line" "$_out" \
            "backup, sync-auth and sudoers features are not available in termux."
        _sess=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'logged out' | head -n1)
        assert_contains "TP-CLI-19 Termux logged out is INFO" "${_sess}" "[INFO]"
        _na=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'features are not available in termux' | head -n1)
        assert_contains "TP-CLI-19 Termux not-available is INFO" "${_na}" "[INFO]"
        assert_contains "TP-CLI-19 Termux logged-out not-available appended" "$_out" \
            "backup features are not available for logged-out environment."
        _after=$(printf '%s\n' "$_out" | tr -d '\r' | grep -A2 "features are not available in termux")
        assert_contains "TP-CLI-19 Termux logged-out line after host line" "${_after}" \
            "not available for logged-out environment."
        assert_not_contains "TP-CLI-19 Termux no backup row" "$_out" "11. backup:"
        assert_not_contains "TP-CLI-19 Termux no sudoers row" "$_out" "sudoers:"
        assert_contains "TP-CLI-19 Termux row 1 is grok-auth" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-19 Termux row 2 is run" "$_out" "2. run:"
        assert_contains "TP-CLI-19 Termux row 5 is language" "$_out" "5. language:"
        assert_not_contains "TP-CLI-19 Termux has no row 6 language" "$_out" "6. language:"
        assert_contains "TP-CLI-19 Termux row 9 is self-management" "$_out" "8. self-management:"
        assert_contains "TP-CLI-19 Termux Exit 0" "$_out" "9. Exit"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="1
0" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-19 Termux auth from-remote is 12" "$_out" \
            "12. sync-auth-from-remote:"
        assert_not_contains "TP-CLI-19 Termux auth hides backup" "$_out" "11. backup:"
        assert_not_contains "TP-CLI-19 Termux auth hides sync-auth" "$_out" "11. sync-auth:"
        assert_not_contains "TP-CLI-19 Termux auth hides sync-auth at 13" "$_out" "13. sync-auth:"
        assert_not_contains "TP-CLI-19 Termux auth hides to-remote when logged out" "$_out" \
            "sync-auth-to-remote:"
        assert_contains "TP-CLI-19 Termux auth add-crontab is 14" "$_out" "14. add-crontab:"
        assert_contains "TP-CLI-19 Termux auth reinstall is 16" "$_out" "16. reinstall:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="6
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-19 Termux pick 6 is not a menu choice" "$_out" "Not a menu choice"
        assert_not_contains "TP-CLI-19 Termux pick 6 does not open language" "$_out" \
            "51. English:"
        assert_not_contains "TP-CLI-19 Termux pick 6 does not open sudoers" "$_out" \
            "1. generate-sudoer-request:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="5
0
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-19 Termux pick 5 opens language" "$_out" "51. English:"
        assert_not_contains "TP-CLI-19 Termux pick 5 is a menu choice" "$_out" "Not a menu choice"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            MSYSTEM="MINGW64" PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-19 Git Bash not-available line" "$_out" \
            "backup, sync-auth and sudoers features are not available in gitbash."
        assert_not_contains "TP-CLI-19 Git Bash no backup row" "$_out" "11. backup:"
        assert_contains "TP-CLI-19 Git Bash row 1 is grok-auth" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-19 Git Bash row 2 is run" "$_out" "2. run:"
        assert_contains "TP-CLI-19 Git Bash row 5 is language" "$_out" "5. language:"
        assert_contains "TP-CLI-19 Git Bash row 9 is self-management" "$_out" "8. self-management:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            OS="Windows_NT" PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-19 Windows cmd not-available line" "$_out" \
            "backup, sync-auth and sudoers features are not available in windows-cmd."
        assert_not_contains "TP-CLI-19 Windows cmd no backup row" "$_out" "11. backup:"
        assert_contains "TP-CLI-19 Windows cmd row 1 is grok-auth" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-19 Windows cmd row 2 is run" "$_out" "2. run:"
        assert_contains "TP-CLI-19 Windows cmd row 5 is language" "$_out" "5. language:"
        assert_contains "TP-CLI-19 Windows cmd row 9 is self-management" "$_out" "8. self-management:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_not_contains "TP-CLI-19 multi-user has no host not-available line" "$_out" \
            "features are not available in"
        assert_contains "TP-CLI-19 multi-user logged-out not-available" "$_out" \
            "backup features are not available for logged-out environment."
        assert_contains "TP-CLI-19 multi-user still lists grok-auth" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-19 multi-user sudoers is 8" "$_out" "7. sudoers:"
        ci_cleanup_env
    else
        t_skip "TP-CLI-19 Termux menu (no python3 for PTY)"
        t_skip "TP-CLI-19 Git Bash menu (no python3 for PTY)"
        t_skip "TP-CLI-19 Windows cmd menu (no python3 for PTY)"
        t_skip "TP-CLI-19 multi-user control (no python3 for PTY)"
    fi

    # TP-CLI-20: logged-in session hides sync-auth / sync-auth-from-remote and
    # appends the logged-in not-available line (does not replace the host line).
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        mkdir -p "${CI_HOME}/.grok"
        cat > "${CI_HOME}/.grok/auth.json" <<'AUTH'
{
  "https://auth.x.ai::test-client": {
    "key": "test-access-token",
    "auth_mode": "oidc",
    "refresh_token": "test-refresh-token",
    "expires_at": "2099-01-01T00:00:00Z"
  }
}
AUTH
        ci_fake_grok_ok
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 multi-user logged in" "$_out" "logged in"
        assert_contains "TP-CLI-20 multi-user logged-in not-available" "$_out" \
            "sync-auth and sync-auth-from-remote features are not available for logged-in environment."
        assert_not_contains "TP-CLI-20 multi-user logged-in has no logged-out line" "$_out" \
            "not available for logged-out environment."
        assert_not_contains "TP-CLI-20 multi-user no host not-available" "$_out" \
            "features are not available in"
        assert_contains "TP-CLI-20 multi-user grok-auth is 1" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-20 multi-user sudoers is 8" "$_out" "7. sudoers:"
        assert_contains "TP-CLI-20 multi-user self-management is 9" "$_out" "8. self-management:"
        assert_not_contains "TP-CLI-20 multi-user no sync-auth row" "$_out" "sync-auth:"
        assert_not_contains "TP-CLI-20 multi-user no from-remote row" "$_out" \
            "sync-auth-from-remote:"
        assert_contains "TP-CLI-20 multi-user Exit 9" "$_out" "9. Exit"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="5
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 pick 5 opens language" "$_out" "51. English:"
        assert_contains "TP-CLI-20 pick 5 lists Greek" "$_out" "63. Ελληνικά:"
        assert_not_contains "TP-CLI-20 pick 5 is a menu choice" "$_out" "Not a menu choice"
        assert_not_contains "TP-CLI-20 pick 5 does not open sudoers" "$_out" \
            "1. generate-sudoer-request:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="7
0" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 listed sudoers number opens submenu" "$_out" \
            "1. generate-sudoer-request:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="sync-auth
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 typed sync-auth is not a menu choice" "$_out" \
            "Not a menu choice"
        assert_not_contains "TP-CLI-20 typed sync-auth does not run skip" "$_out" \
            "No sync-auth for logged-in environment."
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            PTY_IN="1
17
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 logged-in auth lists backup" "$_out" "11. backup:"
        assert_not_contains "TP-CLI-20 logged-in auth has no to-remote row" "$_out" \
            "sync-auth-to-remote:"
        assert_not_contains "TP-CLI-20 logged-in auth hides sync-auth" "$_out" "13. sync-auth:"
        assert_not_contains "TP-CLI-20 logged-in auth hides sync-auth at 11" "$_out" "11. sync-auth:"
        assert_not_contains "TP-CLI-20 logged-in auth has no logged-out line" "$_out" \
            "not available for logged-out environment."
        assert_contains "TP-CLI-20 logged-in auth keeps logged-in line" "$_out" \
            "sync-auth and sync-auth-from-remote features are not available for logged-in environment."
        assert_not_contains "TP-CLI-20 logged-in auth hides from-remote" "$_out" \
            "12. sync-auth-from-remote:"
        assert_contains "TP-CLI-20 logged-in pick 17 is not a menu choice" "$_out" \
            "Not a menu choice"
        assert_not_contains "TP-CLI-20 logged-in pick 17 does not sync" "$_out" \
            "sync-auth complete"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 Termux host not-available kept" "$_out" \
            "backup, sync-auth and sudoers features are not available in termux."
        assert_contains "TP-CLI-20 Termux logged-in not-available appended" "$_out" \
            "sync-auth and sync-auth-from-remote features are not available for logged-in environment."
        _li=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'logged in' | head -n1)
        assert_contains "TP-CLI-20 Termux logged in is INFO" "${_li}" "[INFO]"
        _na2=$(printf '%s\n' "$_out" | tr -d '\r' | grep 'features are not available for logged-in environment' | head -n1)
        assert_contains "TP-CLI-20 Termux logged-in not-available is INFO" "${_na2}" "[INFO]"
        _after=$(printf '%s\n' "$_out" | tr -d '\r' | grep -A2 "logged in")
        assert_contains "TP-CLI-20 Termux host line still under session" "${_after}" \
            "backup, sync-auth and sudoers features are not available in termux."
        assert_contains "TP-CLI-20 Termux logged-in line after host line" "${_after}" \
            "sync-auth and sync-auth-from-remote features are not available for logged-in environment."
        assert_contains "TP-CLI-20 Termux grok-auth is 1" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-20 Termux language is 5" "$_out" "5. language:"
        assert_contains "TP-CLI-20 Termux run is 2" "$_out" "2. run:"
        assert_contains "TP-CLI-20 Termux self-management is 9" "$_out" "8. self-management:"
        assert_not_contains "TP-CLI-20 Termux no from-remote row" "$_out" \
            "sync-auth-from-remote:"
        assert_not_contains "TP-CLI-20 Termux no backup row" "$_out" "11. backup:"
        assert_not_contains "TP-CLI-20 Termux no sudoers row" "$_out" "sudoers:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            MSYSTEM="MINGW64" PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 Git Bash grok-auth is 1" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-20 Git Bash run is 2" "$_out" "2. run:"
        assert_contains "TP-CLI-20 Git Bash self-management is 9" "$_out" "8. self-management:"
        assert_not_contains "TP-CLI-20 Git Bash no from-remote row" "$_out" \
            "sync-auth-from-remote:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            OS="Windows_NT" PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-20 Windows cmd grok-auth is 1" "$_out" "1. grok-auth:"
        assert_contains "TP-CLI-20 Windows cmd run is 2" "$_out" "2. run:"
        assert_contains "TP-CLI-20 Windows cmd self-management is 9" "$_out" "8. self-management:"
        ci_cleanup_env
    else
        t_skip "TP-CLI-20 multi-user logged-in menu (no python3 for PTY)"
        t_skip "TP-CLI-20 Termux logged-in append (no python3 for PTY)"
        t_skip "TP-CLI-20 Git Bash logged-in run first (no python3 for PTY)"
        t_skip "TP-CLI-20 Windows cmd logged-in run first (no python3 for PTY)"
    fi

    # TP-CLI-31: numbered list includes reinstall; setup / update-grok stay off.
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="9" \
            ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-31 multi-user sudoers is 8" "$_out" "7. sudoers:"
        assert_not_contains "TP-CLI-31 top has no setup row" "$_out" "15. setup:"
        assert_not_contains "TP-CLI-31 multi-user no update-grok row" "$_out" "update-grok:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="1
0" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-31 auth reinstall is 16" "$_out" "16. reinstall:"
        assert_contains "TP-CLI-31 auth setup is 15" "$_out" "15. setup:"
        assert_contains "TP-CLI-31 logged-out auth sync-auth is 13" "$_out" "13. sync-auth:"
        assert_not_contains "TP-CLI-31 logged-out hides sync-auth-to-remote" "$_out" \
            "sync-auth-to-remote:"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="1
0" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-31 Termux auth reinstall is 16" "$_out" "16. reinstall:"
        assert_contains "TP-CLI-31 Termux auth setup is 15" "$_out" "15. setup:"
        ci_cleanup_env
    else
        t_skip "TP-CLI-31 multi-user reinstall row (no python3 for PTY)"
        t_skip "TP-CLI-31 Termux reinstall row (no python3 for PTY)"
    fi

    # TP-CLI-32: menu language (thirteen codes). Front 5 / 51-63, save, override, help/about.
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="5
0
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 front row is 5" "$_out" "5. language:"
        assert_not_contains "TP-CLI-32 front has no row 6" "$_out" "6. language:"
        assert_contains "TP-CLI-32 language row 51" "$_out" "51. English:"
        assert_contains "TP-CLI-32 language row 52" "$_out" "52. 简体中文:"
        assert_contains "TP-CLI-32 language row 53" "$_out" "53. 繁體中文:"
        assert_contains "TP-CLI-32 language row 54" "$_out" "54. Español:"
        assert_contains "TP-CLI-32 language row 55" "$_out" "55. العربية:"
        assert_contains "TP-CLI-32 language row 56" "$_out" "56. Français:"
        assert_contains "TP-CLI-32 language row 57" "$_out" "57. Português:"
        assert_contains "TP-CLI-32 language row 58" "$_out" "58. Русский:"
        assert_contains "TP-CLI-32 language row 59" "$_out" "59. Deutsch:"
        assert_contains "TP-CLI-32 language row 60" "$_out" "60. 日本語:"
        assert_contains "TP-CLI-32 language row 61" "$_out" "61. 한국어:"
        assert_contains "TP-CLI-32 language row 62" "$_out" "62. Nederlands:"
        assert_contains "TP-CLI-32 language row 63" "$_out" "63. Ελληνικά:"
        assert_contains "TP-CLI-32 English long" "$_out" "use English for this menu"
        assert_contains "TP-CLI-32 Arabic long" "$_out" "use Arabic for this menu"
        assert_contains "TP-CLI-32 Portuguese long" "$_out" "use Portuguese for this menu"
        assert_contains "TP-CLI-32 Russian long" "$_out" "use Russian for this menu"
        assert_contains "TP-CLI-32 Dutch long" "$_out" "use Dutch for this menu"
        assert_contains "TP-CLI-32 Greek long" "$_out" "use Greek for this menu"
        assert_not_contains "TP-CLI-32 reserved 50 is not printed" "$_out" "50. "
        assert_not_contains "TP-CLI-32 reserved 64 is not printed" "$_out" "64. "
        assert_not_contains "TP-CLI-32 reserved 69 is not printed" "$_out" "69. "
        assert_not_contains "TP-CLI-32 Back does not error" "$_out" "Not a menu choice"
        if [ -f "${CI_HOME}/.local/${APP_NAME}/language" ]; then
            t_fail "TP-CLI-32 Back wrote the language file"
        else
            t_pass "TP-CLI-32 Back did not write the language file"
        fi

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="6
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 front 6 is not a menu choice" "$_out" "Not a menu choice '6'"
        assert_contains "TP-CLI-32 front 6 hint lists row 5" "$_out" "1, 5, 7, 8, or 9 to leave"
        assert_not_contains "TP-CLI-32 front 6 hint does not list row 6" "$_out" "1, 6, 7, 8"
        assert_not_contains "TP-CLI-32 front 6 does not open the board" "$_out" "51. English:"
        if [ -f "${CI_HOME}/.local/${APP_NAME}/language" ]; then
            t_fail "TP-CLI-32 front 6 wrote the language file"
        else
            t_pass "TP-CLI-32 front 6 did not write the language file"
        fi

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="5
50
64
69
0
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 reserved 50 warns" "$_out" "Not a menu choice '50'"
        assert_contains "TP-CLI-32 reserved 64 warns" "$_out" "Not a menu choice '64'"
        assert_contains "TP-CLI-32 reserved 69 warns" "$_out" "Not a menu choice '69'"
        assert_contains "TP-CLI-32 reserved reprint still lists 51" "$_out" "51. English:"
        if [ -f "${CI_HOME}/.local/${APP_NAME}/language" ]; then
            t_fail "TP-CLI-32 reserved picks wrote the language file"
        else
            t_pass "TP-CLI-32 reserved picks did not write the language file"
        fi

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="5
53
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 saved Traditional Chinese" "$_out" "選單語言是繁體中文"
        assert_contains "TP-CLI-32 front redraws in Traditional Chinese" "$_out" "5. 語言:"
        _langf="${CI_HOME}/.local/${APP_NAME}/language"
        assert_eq "TP-CLI-32 language file is zh-Hant" "zh-Hant" "$(head -n 1 "${_langf}")"
        _mode=$(stat -c '%a' "${_langf}" 2>/dev/null || stat -f '%OLp' "${_langf}")
        assert_eq "TP-CLI-32 language file mode 0600" "600" "${_mode}"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 next run keeps Traditional Chinese" "$_out" "5. 語言:"
        assert_not_contains "TP-CLI-32 next run is not the English short" "$_out" "5. language:"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_CLI_LANG=ja \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 GROK_CLI_LANG ja" "$_out" "5. 言語:"
        assert_eq "TP-CLI-32 override does not rewrite the file" "zh-Hant" "$(head -n 1 "${_langf}")"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="5
63
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 saved Greek" "$_out" "Η γλώσσα του μενού είναι ελληνικά"
        assert_contains "TP-CLI-32 front redraws in Greek" "$_out" "5. γλώσσα:"
        assert_eq "TP-CLI-32 language file is el" "el" "$(head -n 1 "${_langf}")"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="5
arabic
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 saved Arabic" "$_out" "لغة القائمة هي العربية"
        assert_contains "TP-CLI-32 front redraws in Arabic" "$_out" "5. لغة:"
        assert_eq "TP-CLI-32 language file is ar" "ar" "$(head -n 1 "${_langf}")"

        _help=$(HOME="${CI_HOME}" GROK_CLI_LANG=ja sh "${SCRIPT}" help 2>/dev/null)
        assert_contains "TP-CLI-32 ja help heading" "${_help}" "使い方:"
        assert_contains "TP-CLI-32 ja help keeps install" "${_help}" "install"
        assert_contains "TP-CLI-32 ja help names GROK_CLI_LANG" "${_help}" "GROK_CLI_LANG"
        _about=$(HOME="${CI_HOME}" GROK_CLI_LANG=ja sh "${SCRIPT}" about 2>/dev/null)
        assert_contains "TP-CLI-32 ja about title" "${_about}" "概要 / 診断"
        assert_contains "TP-CLI-32 ja about cache" "${_about}" "使用中のキャッシュフォルダ:"
        _json=$(HOME="${CI_HOME}" GROK_CLI_LANG=ja sh "${SCRIPT}" --json about 2>/dev/null)
        assert_contains "TP-CLI-32 json about stays English keys" "${_json}" '"cache_used"'
        assert_not_contains "TP-CLI-32 json about has no Japanese title" "${_json}" "概要"
        _help_el=$(HOME="${CI_HOME}" GROK_CLI_LANG=el sh "${SCRIPT}" help 2>/dev/null)
        assert_contains "TP-CLI-32 el help heading" "${_help_el}" "Χρήση:"
        _help_en=$(HOME="${CI_HOME}" GROK_CLI_LANG=en sh "${SCRIPT}" help 2>/dev/null)
        assert_contains "TP-CLI-32 en help lists thirteen codes" "${_help_en}" \
            "en zh-Hans zh-Hant es ar fr pt ru de ja ko nl el"
        assert_contains "TP-CLI-32 en help names row 5" "${_help_en}" \
            "Menu row 5 sets the display language (51 English through 63 Greek)."

        _err=$(HOME="${CI_HOME}" sh "${SCRIPT}" language 2>&1 >/dev/null)
        assert_eq "TP-CLI-32 language is not an argv verb" 1 "$?"
        assert_contains "TP-CLI-32 language argv unknown" "${_err}" "Unknown command"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_CLI_LANG=en \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-32 Termux still lists language" "$_out" "5. language:"
        ci_cleanup_env
    else
        t_skip "TP-CLI-32 language board (no python3 for PTY)"
        t_skip "TP-CLI-32 save and next run (no python3 for PTY)"
        t_skip "TP-CLI-32 help and about (no python3 for PTY)"
    fi

    # TP-CLI-21: Termux menu uses local auth cookies (no live grok -p hello).
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        ci_fake_grok_hang
        _start=$(date +%s)
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            GROK_PROMPT_TIMEOUT=1 GROK_PROMPT_KILL_AFTER=1 \
            PTY_TIMEOUT=12 PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        _elapsed=$(($(date +%s) - _start))
        assert_contains "TP-CLI-21 Termux hang-grok still prints menu" "$_out" "9. Exit"
        assert_not_contains "TP-CLI-21 Termux no live checking-session" "$_out" \
            "checking session (grok -p hello, timeout"
        assert_contains "TP-CLI-21 Termux hang-grok logged out" "$_out" "logged out"
        assert_not_contains "TP-CLI-21 Termux hang-grok not timeout" "$_out" "timeout"
        assert_contains "TP-CLI-21 Termux hang-grok not-available line" "$_out" \
            "backup, sync-auth and sudoers features are not available in termux."
        assert_contains "TP-CLI-21 Termux hang-grok Choice prompt" "$_out" "Choice:"
        if [ "${_elapsed}" -lt 5 ]; then
            t_pass "TP-CLI-21 Termux menu did not freeze (${_elapsed}s)"
        else
            t_fail "TP-CLI-21 Termux menu froze for ${_elapsed}s"
        fi

        # TP-CLI-22: a bad pick reprints the list; live grok -p hello is not used.
        _plog="${CI_HOME}/probe.log"
        rm -f "${_plog}"
        _start=$(date +%s)
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            GROK_PROMPT_TIMEOUT=1 GROK_PROMPT_KILL_AFTER=1 \
            GROK_PROBE_LOG="${_plog}" \
            PTY_TIMEOUT=12 PTY_IN="12
9" ci_pty_capture "${SCRIPT}" menu)
        _elapsed=$(($(date +%s) - _start))
        _nprobe=$(wc -l < "${_plog}" 2>/dev/null | tr -d ' ')
        [ -n "${_nprobe}" ] || _nprobe=0
        assert_contains "TP-CLI-22 bad pick not a menu choice" "$_out" "Not a menu choice"
        assert_contains "TP-CLI-22 reprint still Exit 9" "$_out" "9. Exit"
        assert_eq "TP-CLI-22 hang grok not live-probed" "0" "${_nprobe}"
        if [ "${_elapsed}" -lt 12 ]; then
            t_pass "TP-CLI-22 reprint did not re-probe (${_elapsed}s, probes=${_nprobe})"
        else
            t_fail "TP-CLI-22 reprint froze for ${_elapsed}s (probes=${_nprobe})"
        fi
        ci_cleanup_env
    else
        t_skip "TP-CLI-21 Termux hang-grok menu (no python3 for PTY)"
        t_skip "TP-CLI-22 Termux reprint cache (no python3 for PTY)"
    fi

    # TP-CLI-30: invalid choice at any menu layer retries that layer
    # (out_error + reprint; MUST NOT out_die / unknown argv). Portable
    # proof mold names this TP-CLI-19; this product already assigned
    # TP-CLI-19 to this-login-only host menu.
    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="4
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-30 main unused 4 is ERROR" "$_out" "[ERROR]"
        assert_contains "TP-CLI-30 main unused 4 names pick" "$_out" "Not a menu choice '4'"
        assert_not_contains "TP-CLI-30 main unused 4 not unknown argv" "$_out" "Unknown command"
        _nchoice=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c 'Choice:' || true)
        assert_eq "TP-CLI-30 main unused 4 reprints Choice" "2" "${_nchoice}"
        _nbackup=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c '1. grok-auth:' || true)
        assert_eq "TP-CLI-30 main unused 4 reprints main list" "2" "${_nbackup}"
        assert_contains "TP-CLI-30 main unused 4 still Exit 9" "$_out" "9. Exit"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="nope
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-30 main unknown name is ERROR" "$_out" "[ERROR]"
        assert_contains "TP-CLI-30 main unknown name names pick" "$_out" "Not a menu choice 'nope'"
        _nchoice=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c 'Choice:' || true)
        assert_eq "TP-CLI-30 main unknown name reprints Choice" "2" "${_nchoice}"

        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" \
            PTY_IN="7
6
0
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-30 submenu unused 6 is ERROR" "$_out" "[ERROR]"
        assert_contains "TP-CLI-30 submenu unused 6 names pick" "$_out" "Not a menu choice '6'"
        assert_not_contains "TP-CLI-30 submenu unused 6 not unknown argv" "$_out" "Unknown command"
        _ngen=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c '1. generate-sudoer-request:' || true)
        assert_eq "TP-CLI-30 submenu unused 6 reprints sudoers list" "2" "${_ngen}"
        _nback=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c '0. Back' || true)
        assert_eq "TP-CLI-30 submenu unused 6 still Back" "2" "${_nback}"

        mkdir -p "${CI_HOME}/.grok"
        cat > "${CI_HOME}/.grok/auth.json" <<'AUTH'
{
  "https://auth.x.ai::test-client": {
    "key": "test-access-token",
    "auth_mode": "oidc",
    "refresh_token": "test-refresh-token",
    "expires_at": "2099-01-01T00:00:00Z"
  }
}
AUTH
        ci_fake_grok_ok
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" GROK_BIN="${GROK_BIN}" \
            TERMUX_VERSION="test" PREFIX="/data/data/com.termux/files/usr" \
            PTY_IN="6
9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-30 Termux logged-in unused 6 is ERROR" "$_out" "[ERROR]"
        assert_contains "TP-CLI-30 Termux logged-in unused 6 names pick" "$_out" "Not a menu choice '6'"
        assert_not_contains "TP-CLI-30 Termux logged-in unused 6 does not open language" "$_out" \
            "51. English:"
        assert_not_contains "TP-CLI-30 Termux logged-in unused 6 does not open sudoers" "$_out" \
            "1. generate-sudoer-request:"
        _nchoice=$(printf '%s\n' "$_out" | tr -d '\r' | grep -c 'Choice:' || true)
        assert_eq "TP-CLI-30 Termux logged-in unused 6 reprints Choice" "2" "${_nchoice}"
        ci_cleanup_env
    else
        t_skip "TP-CLI-30 main unused 4 (no python3 for PTY)"
        t_skip "TP-CLI-30 main unknown name (no python3 for PTY)"
        t_skip "TP-CLI-30 sudoers submenu unused 6 (no python3 for PTY)"
        t_skip "TP-CLI-30 Termux logged-in unused 6 (no python3 for PTY)"
    fi

    # TP-CLI-23: ship unit always bounds the probe (timeout -k + watchdog).
    _src=$(cat "${SCRIPT}")
    assert_contains "TP-CLI-23 bounded helper" "${_src}" "gc_grok_prompt_run_bounded"
    assert_contains "TP-CLI-23 GNU timeout -k" "${_src}" 'timeout -k'
    assert_contains "TP-CLI-23 watchdog SIGKILL" "${_src}" "kill -9"
    assert_contains "TP-CLI-23 PRoot reaper helper" "${_src}" "gc_grok_p_once_run"
    assert_contains "TP-CLI-23 PRoot dispatch" "${_src}" 'command -v proot'
    assert_contains "TP-CLI-23 reaper setsid collector" "${_src}" "setsid"
    assert_contains "TP-CLI-23 reaper ignores TSTP" "${_src}" "trap '' TSTP"
    assert_contains "TP-CLI-23 wait reaper first" "${_src}" 'wait "${_preap}"'
    assert_contains "TP-CLI-23 menu checking session line" "${_src}" "checking session (grok -p hello, timeout"
    assert_contains "TP-CLI-23 default GROK_PROMPT_TIMEOUT 14" "${_src}" 'GROK_PROMPT_TIMEOUT:=14'
    assert_contains "TP-CLI-23 timeout status word" "${_src}" 'GC_GROK_PROMPT_STATUS="timeout"'
    assert_contains "TP-CLI-23 menu prints timeout" "${_src}" 'out_info "timeout"'
    assert_contains "TP-CLI-23 menu prints logged in" "${_src}" 'out_info "logged in"'
    assert_contains "TP-CLI-23 menu prints logged out" "${_src}" 'out_info "logged out"'
    assert_contains "TP-CLI-23 host not-available is INFO" "${_src}" \
        'out_info "backup, sync-auth and sudoers features are not available in'
    assert_contains "TP-CLI-23 logged-in not-available is INFO" "${_src}" \
        'out_info "sync-auth and sync-auth-from-remote features are not available for logged-in environment."'
    assert_contains "TP-CLI-23 logged-out not-available is INFO" "${_src}" \
        'out_info "backup features are not available for logged-out environment."'
    assert_not_contains "TP-CLI-23 no out_plain timeout" "${_src}" 'out_plain "timeout"'
    assert_not_contains "TP-CLI-23 no out_plain logged in" "${_src}" 'out_plain "logged in"'
    assert_not_contains "TP-CLI-23 no out_plain logged out" "${_src}" 'out_plain "logged out"'
    assert_not_contains "TP-CLI-23 no out_plain host not-available" "${_src}" \
        'out_plain "backup, sync-auth and sudoers features are not available'
    assert_not_contains "TP-CLI-23 no out_plain logged-in not-available" "${_src}" \
        'out_plain "sync-auth and sync-auth-from-remote features are not available'
    assert_not_contains "TP-CLI-23 no out_plain logged-out not-available" "${_src}" \
        'out_plain "backup features are not available'
    assert_contains "TP-CLI-23 local-auth helper" "${_src}" "gc_session_uses_local_auth"
    assert_contains "TP-CLI-23 local-auth cookies helper" "${_src}" "gc_session_from_local_auth"
    assert_contains "TP-CLI-23 timeout env protected" "${_src}" "DO NOT REMOVE GROK_PROMPT_TIMEOUT"

    # TP-CLI-25 / 26 / 27 / 28: --debug menu elapsed (internal-timer).
    _src=$(cat "${SCRIPT}")
    assert_contains "TP-CLI-28 util_int_timer_start" "${_src}" "util_int_timer_start"
    assert_contains "TP-CLI-28 util_int_timer_stop" "${_src}" "util_int_timer_stop"
    assert_contains "TP-CLI-28 util_int_timer_status" "${_src}" "util_int_timer_status"
    assert_contains "TP-CLI-28 util_int_timer_elapsed" "${_src}" "util_int_timer_elapsed"
    assert_contains "TP-CLI-28 util_int_timer_reset" "${_src}" "util_int_timer_reset"
    assert_contains "TP-CLI-28 util_int_timer_kill" "${_src}" "util_int_timer_kill"
    assert_contains "TP-CLI-28 util_int_timer_list" "${_src}" "util_int_timer_list"
    _help=$(sh "${SCRIPT}" help 2>/dev/null)
    assert_contains "TP-CLI-28 help --debug" "${_help}" "--debug"
    assert_not_contains "TP-CLI-28 help no timer start verb" "${_help}" "start [name]"
    unset _help

    # AC-6: source helpers (no app_main) and fail-close a second start of the same name.
    _snip=$(mktemp)
    sed '/^app_main "\$@"$/d' "${SCRIPT}" > "${_snip}"
    _ac6=$(HOME="${HOME:-/tmp}" sh -c '
        set -u
        . "$1"
        UTIL_INT_TIMER_MAP=""
        util_int_timer_start ac6
        printf "ec1=%s\n" "$?"
        _map1="${UTIL_INT_TIMER_MAP}"
        case "${_map1}" in
            ac6=*[0-9]*) printf "map1_ok=1\n" ;;
            *) printf "map1_ok=0\n" ;;
        esac
        util_int_timer_start ac6
        printf "ec2=%s\n" "$?"
        if [ "${UTIL_INT_TIMER_MAP}" = "${_map1}" ]; then
            printf "same_map=1\n"
        else
            printf "same_map=0\n"
        fi
        util_int_timer_start "foo[ab]"
        printf "ec_brack=%s\n" "$?"
        util_int_timer_start "a;b"
        printf "ec_semi=%s\n" "$?"
        util_int_timer_start "x&y"
        printf "ec_amp=%s\n" "$?"
        DEBUG=1
        util_int_timer_debug_begin ac6
        printf "dbg=%s\n" "$?"
    ' _ "${_snip}" 2>/dev/null)
    rm -f "${_snip}"
    assert_contains "TP-CLI-28 AC-6 first start ok" "${_ac6}" "ec1=0"
    assert_contains "TP-CLI-28 AC-6 map has epoch" "${_ac6}" "map1_ok=1"
    assert_contains "TP-CLI-28 AC-6 double-start fail-closed" "${_ac6}" "ec2=1"
    assert_contains "TP-CLI-28 AC-6 epoch unchanged" "${_ac6}" "same_map=1"
    assert_contains "TP-CLI-28 invalid name bracket" "${_ac6}" "ec_brack=1"
    assert_contains "TP-CLI-28 invalid name semicolon" "${_ac6}" "ec_semi=1"
    assert_contains "TP-CLI-28 invalid name ampersand" "${_ac6}" "ec_amp=1"
    assert_contains "TP-CLI-28 debug wrapper still 0 after reset-then-start" "${_ac6}" "dbg=0"
    unset _ac6 _snip

    _json=$(sh "${SCRIPT}" --json --debug version 2>/dev/null)
    _jec=$?
    assert_eq "TP-CLI-27 --json --debug version exit 0" 0 "${_jec}"
    assert_contains "TP-CLI-27 --json --debug stdout type" "${_json}" '"type":"version"'
    assert_not_contains "TP-CLI-27 --json --debug no DEBUG on stdout" "${_json}" "[DEBUG]"
    assert_not_contains "TP-CLI-27 --json --debug no menu step on stdout" "${_json}" "menu step"
    unset _json _jec

    if command -v python3 >/dev/null 2>&1; then
        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="9" ci_pty_capture "${SCRIPT}" --debug menu)
        assert_contains "TP-CLI-25 debug menu still Exit 9" "$_out" "9. Exit"
        assert_contains "TP-CLI-25 debug menu Choice" "$_out" "Choice:"
        for _st in paint header session host logged-in rows; do
            assert_contains "TP-CLI-25 menu step ${_st} start" "$_out" "menu step ${_st}: start"
            assert_contains "TP-CLI-25 menu step ${_st} elapsed" "$_out" "menu step ${_st}: elapsed"
        done
        assert_not_contains "TP-CLI-25 elapsed not on choice row" "$_out" "1. grok-auth: elapsed"
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="7
9" ci_pty_capture "${SCRIPT}" --debug menu)
        assert_contains "TP-CLI-25 debug submenu still Exit 9" "$_out" "9. Exit"
        for _st in sudoers.paint sudoers.header sudoers.rows; do
            assert_contains "TP-CLI-25 menu step ${_st} start" "$_out" "menu step ${_st}: start"
            assert_contains "TP-CLI-25 menu step ${_st} elapsed" "$_out" "menu step ${_st}: elapsed"
        done
        assert_not_contains "TP-CLI-25 submenu elapsed not on choice row" "$_out" \
            "1. generate-sudoer-request: elapsed"
        ci_cleanup_env

        ci_isolated_env
        _out=$(HOME="${CI_HOME}" GROK_HOME="${CI_HOME}/.grok" PTY_IN="9" ci_pty_capture "${SCRIPT}" menu)
        assert_contains "TP-CLI-26 no-debug still Exit 9" "$_out" "9. Exit"
        assert_contains "TP-CLI-26 no-debug checking session" "$_out" "checking session (grok -p hello, timeout"
        assert_not_contains "TP-CLI-26 no menu step start" "$_out" "menu step "
        assert_not_contains "TP-CLI-26 no DEBUG tag" "$_out" "[DEBUG]"
        ci_cleanup_env
    else
        t_skip "TP-CLI-25 --debug menu elapsed (no python3 for PTY)"
        t_skip "TP-CLI-26 no-debug menu (no python3 for PTY)"
    fi

    # TP-CLI-18: Active requirement bodies must not freeze a session Unix login
    # Needle is split so this test file is not itself a login leak.
    _needle="leo""lio"
    _hit=""
    for _rf in "${REPO_ROOT}/docs/requirements"/requirement-*.md; do
        case "$_rf" in
            *requirement-domain-folder-backup.md|*requirement-folder-archive-backup.md|*requirement-folder-archive-backup-retention-*) continue ;;
        esac
        if grep -F "$_needle" "$_rf" >/dev/null 2>&1; then
            _hit="${_hit} ${_rf##*/}"
        fi
    done
    if [ -z "$_hit" ]; then
        t_pass "TP-CLI-18 Active REQs do not freeze a session Unix login in samples"
    else
        t_fail "TP-CLI-18 frozen session login in:${_hit}"
    fi
}
