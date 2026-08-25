#!/usr/bin/env bash

LOG_FILE="/var/log/system_health.log"
DISK_WARN_THRESHOLD=80
PING_HOST="google.com"
PING_COUNT=2
SERVICES=("sshd" "apache2" "nginx" "cron")

RED='\033[0;31m'
YEL='\033[0;33m'
GRN='\033[0;32m'
CYN='\033[0;36m'
BLD='\033[1m'
RST='\033[0m'

section()  { printf "\n${BLD}${CYN}>>> %s${RST}\n" "$1"; }
ok()       { printf "  ${GRN}[OK]${RST}  %s\n" "$1"; }
warn()     { printf "  ${YEL}[WARN]${RST} %s\n" "$1"; }
fail()     { printf "  ${RED}[FAIL]${RST} %s\n" "$1"; }

strip_color() { sed 's/\x1b\[[0-9;]*m//g'; }

build_report() {

TIMESTAMP=$(date)
HOSTNAME=$(hostname)
UPTIME=$(uptime -p 2>/dev/null || uptime | awk -F'up ' '{print $2}' | cut -d',' -f1,2)
OS=$(lsb_release -d 2>/dev/null | awk -F'\t' '{print $2}' || uname -o)
KERNEL=$(uname -r)

printf "\n${BLD}========================================${RST}\n"
printf "${BLD}       SYSTEM HEALTH REPORT             ${RST}\n"
printf "${BLD}========================================${RST}\n"
printf "  Date     : %s\n" "$TIMESTAMP"
printf "  Hostname : %s\n" "$HOSTNAME"
printf "  OS       : %s\n" "$OS"
printf "  Kernel   : %s\n" "$KERNEL"
printf "  Uptime   : %s\n" "$UPTIME"
printf "${BLD}========================================${RST}\n"

section "CPU USAGE"

CPU_LINE=$(grep -m1 '^cpu ' /proc/stat)
read -r _ user nice system idle iowait irq softirq rest <<< "$CPU_LINE"
TOTAL=$((user + nice + system + idle + iowait + irq + softirq))
IDLE_PCT=$((idle * 100 / TOTAL))
USED_PCT=$((100 - IDLE_PCT))
printf "  Overall CPU used : ${BLD}%d%%${RST}\n" "$USED_PCT"

printf "\n  Top 5 processes by CPU:\n"
printf "  %-8s %-6s %s\n" "PID" "CPU%%" "COMMAND"
ps -eo pid,pcpu,comm --sort=-pcpu 2>/dev/null | head -6 | tail -5 | \
  while read -r pid pcpu cmd; do
    printf "  %-8s %-6s %s\n" "$pid" "$pcpu" "$cmd"
  done

section "MEMORY USAGE"
MEM_RAW=$(free -h 2>/dev/null)
MEM_TOTAL=$(echo "$MEM_RAW" | awk '/^Mem:/ {print $2}')
MEM_USED=$( echo "$MEM_RAW" | awk '/^Mem:/ {print $3}')
MEM_FREE=$( echo "$MEM_RAW" | awk '/^Mem:/ {print $4}')
SWAP_TOTAL=$(echo "$MEM_RAW" | awk '/^Swap:/ {print $2}')
SWAP_USED=$( echo "$MEM_RAW" | awk '/^Swap:/ {print $3}')

printf "  RAM  : used ${BLD}%s${RST} / total ${BLD}%s${RST}  (free: %s)\n" \
       "$MEM_USED" "$MEM_TOTAL" "$MEM_FREE"
printf "  Swap : used ${BLD}%s${RST} / total ${BLD}%s${RST}\n" \
       "$SWAP_USED" "$SWAP_TOTAL"

section "DISK USAGE"
printf "  %-25s %5s %5s %5s %6s  %s\n" \
       "Filesystem" "Size" "Used" "Avail" "Use%" "Mount"

DISK_ALERT=0
while IFS= read -r line; do
  [[ "$line" == Filesystem* ]] && continue

  MOUNT=$(echo "$line" | awk '{print $NF}')
  USE_PCT=$(echo "$line" | awk '{print $5}' | tr -d '%')
  FS=$(echo "$line"  | awk '{print $1}')
  SIZE=$(echo "$line" | awk '{print $2}')
  USED=$(echo "$line" | awk '{print $3}')
  AVAIL=$(echo "$line" | awk '{print $4}')

  if [[ "$USE_PCT" -ge "$DISK_WARN_THRESHOLD" ]] 2>/dev/null; then
    printf "  ${RED}%-25s %5s %5s %5s %5s%%  %s  [HIGH]${RST}\n" \
           "$FS" "$SIZE" "$USED" "$AVAIL" "$USE_PCT" "$MOUNT"
    DISK_ALERT=1
  else
    printf "  ${GRN}%-25s %5s %5s %5s %5s%%  %s${RST}\n" \
           "$FS" "$SIZE" "$USED" "$AVAIL" "$USE_PCT" "$MOUNT"
  fi
done < <(df -h --output=source,size,used,avail,pcent,target 2>/dev/null \
         | grep -v '^Filesystem\|tmpfs\|udev\|loop' \
         || df -h | tail -n +2)

[[ "$DISK_ALERT" -eq 1 ]] && \
  warn "One or more partitions exceed ${DISK_WARN_THRESHOLD}% usage!"

section "NETWORK STATUS"

IFACES=$(ip -4 addr show 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' \
         | awk '{print $NF": "$2}')
if [[ -z "$IFACES" ]]; then
  IFACES=$(ifconfig 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' \
           | awk '{print $NF": "$2}' || echo "N/A")
fi

printf "  Interfaces:\n"
while IFS= read -r iface; do
  printf "    %s\n" "$iface"
done <<< "$IFACES"

printf "\n  Connectivity test (ping %s x%d):\n" "$PING_HOST" "$PING_COUNT"
if ping -c "$PING_COUNT" -W 3 "$PING_HOST" &>/dev/null; then
  ok "Internet reachable — ping $PING_HOST succeeded"
else
  fail "Cannot reach $PING_HOST — no internet or DNS issue"
fi

section "SERVICE STATUS"
for svc in "${SERVICES[@]}"; do
  if command -v systemctl &>/dev/null; then
    STATE=$(systemctl is-active "$svc" 2>/dev/null)
    if [[ "$STATE" == "active" ]]; then
      ok "$svc — active (running)"
    elif [[ "$STATE" == "inactive" ]]; then
      warn "$svc — inactive (stopped)"
    else
      fail "$svc — $STATE (not found or error)"
    fi
  else
    if pgrep -x "$svc" &>/dev/null; then
      ok "$svc — process found"
    else
      warn "$svc — process not found"
    fi
  fi
done

printf "\n${BLD}========================================${RST}\n"
printf "  Report saved to: ${CYN}%s${RST}\n" "$LOG_FILE"
printf "${BLD}========================================${RST}\n\n"

}

write_log() {
  local LOG_DIR
  LOG_DIR=$(dirname "$LOG_FILE")

  if ! mkdir -p "$LOG_DIR" 2>/dev/null || ! touch "$LOG_FILE" 2>/dev/null; then
    LOG_FILE="$HOME/system_health.log"
    printf "${YEL}[WARN]${RST} No write access to /var/log — saving to %s instead.\n" \
           "$LOG_FILE"
    touch "$LOG_FILE"
  fi

  {
    echo ""
    echo "============================================================"
    echo " SYSTEM HEALTH REPORT — $(date)"
    echo "============================================================"
    build_report | strip_color
  } >> "$LOG_FILE"
}

main() {
  build_report
  write_log
  printf "Done. Full log at: ${CYN}%s${RST}\n\n" "$LOG_FILE"
}

main "$@"
