#!/bin/bash

WS=/tmp/captcha-bypas-test-fifo

rm -f "$WS"
mkfifo "$WS"

while read -r msg; do
  type="$(jq -r '.type' <<< "$msg")"

  if [ "$type" == 'challenge' ]; then
    challenge="$(jq -r '.value' <<< "$msg")"

    # solve using metadata
    value1="$(calc "$(base64 -d <<< "$challenge" | \
      strings | \
      grep -o '[0-9]\+ / [0-9]\+ + [0-9]\+^[0-9]\+')")"

    # solve using image to text
    value2="$(calc "$(base64 -d <<< "$challenge" | \
      tesseract - - 2>/dev/null | \
      sed 's/["%/4]\(.\)$/^\1/')" 2>/dev/null)"

    # tesseract is particularly bad at recognizing `^``, mostly confusing it for
    # `4`, `%`, `/` and `"`, which should explain the sed expression above.
    # However, it still usually takes a good hand full of tries to get this
    # right using tesseract :/

    # Though, just to prove that both ways work, we only submit an answer once
    # both methods agree
    if [ "$value1" == "$value2" ]; then
      echo '{"type":"response"}' | jq -c ".value = \"${value1:1}\"" > "$WS"
    fi

  elif [ "$type" == 'success' ]; then
    value="$(jq -r '.value' <<< "$msg")"
    echo "$value" | grep -o 'TG23{.*}'
    exit
  else
    echo "$type"
  fi
done < <(websocat ws://localhost:3000/2 < <(cat "$WS"))

rm "$WS"
