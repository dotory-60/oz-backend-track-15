#!/usr/bin/env zsh
set -u
set -o pipefail

URL='http://127.0.0.1:8000/'
HEADERS=(-H 'accept: application/json')
TOTAL=1000

typeset -i ok=0
typeset -i fail=0

for i in {1..1000}; do
    # HTTP 코드만 출력받고 본문은 버림
    code=$(curl -sS -o /dev/null -w '%{http_code}' -X GET "$URL" "${HEADERS[@]}") || code=0

    if [[ "$code" -ge 200 && "$code" -lt 400 ]]; then
        ((ok++))
    else
        ((fail++))
    fi

    # 100회 단위 진행 상황 표시
    if (( i % 100 == 0 )); then
        print -r -- "Progress: $i/$TOTAL  ok=$ok  fail=$fail  (last=$code)"
    fi
done

print -r -- "Done: total=$TOTAL  ok=$ok  fail=$fail"
exit $(( fail > 0 ? 1 : 0 ))
