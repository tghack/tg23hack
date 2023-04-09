#!/bin/bash

WS=/tmp/captcha-bypas-test-fifo

rm -f "$WS"
mkfifo "$WS"

while read -r msg; do
  type="$(jq -r '.type' <<< "$msg")"

  if [ "$type" == 'challenge' ]; then
    challenge="$(jq -r '.value' <<< "$msg")"

    value="$(base64 -d <<< "$challenge" | \
      od -tx1 -An -j24 | \
      tr -d '\n' | \
      tr -d '*' | \
      grep -o '\(9\|8\)0 .. ..' | \
      sed 's/^.. .. 5f/1/' | \
      sed 's/^.. .. 20/0/' | \
      tr -d '\n' | \
      fold -w8 | \
      while read -r w; do printf '%02x' "$((2#$w))"; done | \
      xxd -r -p | \
      tr -d '\0')"

    echo '{"type":"response"}' | jq -c ".value = \"${value}\"" > "$WS"

  elif [ "$type" == 'success' ]; then
    value="$(jq -r '.value' <<< "$msg")"
    echo "$value" | grep -o 'TG23{.*}'
    exit
  else
    echo "$type"
  fi
done < <(websocat ws://localhost:3000/5 < <(cat "$WS"))

rm "$WS"
