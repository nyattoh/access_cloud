#!/bin/bash

SESSION="test-multiroom-company"
ROOMS=("Alpha Room" "Beta Room")
ORGS=("org-01" "org-02" "org-03" "org-04")
ROLES=("pm" "worker-a" "worker-b" "worker-c")

tmux new-session -d -s "$SESSION" -n "${ROOMS[0]}"

for w in "${!ROOMS[@]}"; do
  if [ "$w" -ne 0 ]; then
    tmux new-window -t "$SESSION:" -n "${ROOMS[$w]}"
  fi
  WIN="${SESSION}:${w}"

  for o in "${!ORGS[@]}"; do
    if [ "$o" -ne 0 ]; then
      tmux split-window -t "$WIN" -h
      tmux select-layout -t "$WIN" tiled
    fi
    PANE="$WIN.$o"
    # orgごとに4ペイン
    for r in "${!ROLES[@]}"; do
      if [ "$r" -ne 0 ]; then
        tmux split-window -t "$PANE" -v
        tmux select-layout -t "$WIN" tiled
      fi
      # ここで各ペインにコマンドを送る場合は下記
      # tmux send-keys -t "$PANE.$r" "echo ${ORGS[$o]} ${ROLES[$r]}" C-m
    done
  done
  tmux select-layout -t "$WIN" tiled
done

tmux select-window -t "$SESSION:0"
tmux attach-session -t "$SESSION"