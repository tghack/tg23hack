#!/bin/bash

WS=/tmp/captcha-bypas-test-fifo

rm -f "$WS"
mkfifo "$WS"

while read -r msg; do
  type="$(jq -r '.type' <<< "$msg")"

  if [ "$type" == 'challenge' ]; then
    challenge="$(jq -r '.value' <<< "$msg")"

    value="$(base64 -d <<< "$challenge" | \
      convert - RGBA:- | \
      od --endian=big -tx4 -An | \
      grep -o ffd700ff | \
      wc -l)"

    echo '{"type":"response"}' | jq -c ".value = \"${value}\"" > "$WS"

  elif [ "$type" == 'success' ]; then
    value="$(jq -r '.value' <<< "$msg")"
    echo "$value" | grep -o 'TG23{.*}'
    exit
  else
    echo "$type"
  fi
done < <(websocat ws://localhost:3000/4 < <(cat "$WS"))

rm "$WS"
