# Pomodoro Timer
Pomodoro timer to be used with tmux.

Use (.tmux.conf):
```
bind-key C-r run-shell -b 'python ~/path/to/source/pomodoro.py -r'
set -g status-left-length 45
set -g status-left '#[fg=colour3,bg=colour0,nobold] #(eval python ~/path/to/source/pomodoro.py)'
set -g status-interval 1
run-shell -b 'python pomodoro.py -r'
```
