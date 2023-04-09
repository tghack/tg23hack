#!/bin/bash

WS=/tmp/captcha-bypas-test-fifo

rm -f "$WS"
mkfifo "$WS"

while read -r msg; do
  type="$(jq -r '.type' <<< "$msg")"

  if [ "$type" == 'challenge' ]; then
    challenge="$(jq -r '.value' <<< "$msg")"

    value="$(base64 -d <<< "$challenge" | zbarimg -q --raw -)"

    echo '{"type":"response"}' | jq -c ".value = \"${value}\"" > "$WS"

  elif [ "$type" == 'success' ]; then
    value="$(jq -r '.value' <<< "$msg")"
    echo "$value" | grep -o 'TG23{.*}'
    exit
  else
    echo "$type"
  fi
done < <(websocat ws://localhost:3000/3 < <(cat "$WS"))

rm "$WS"
