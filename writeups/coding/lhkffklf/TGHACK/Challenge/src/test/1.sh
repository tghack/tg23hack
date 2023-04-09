#!/bin/bash

WS=/tmp/captcha-bypas-test-fifo

rm -f "$WS"
mkfifo "$WS"

while read -r msg; do
  type="$(jq -r '.type' <<< "$msg")"

  if [ "$type" == 'challenge' ]; then
    challenge="$(jq -r '.value' <<< "$msg")"
    value="$(calc "$challenge")"
    echo '{"type":"response"}' | jq -c ".value = \"${value:1}\"" > "$WS"
  elif [ "$type" == 'success' ]; then
    value="$(jq -r '.value' <<< "$msg")"
    echo "$value" | grep -o 'TG23{.*}'
    exit
  else
    echo "$type"
  fi
done < <(websocat ws://localhost:3000/1 < <(cat "$WS"))

rm "$WS"
