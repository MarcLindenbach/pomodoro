# Pomodoro Timer
Pomodoro timer to be used with tmux.

## To use
Make sure you have cowsay install `apt install cowsay`. Update your
`.tmux.conf` file with the following:
```
bind-key C-r run-shell -b 'python ~/path/to/source/pomodoro.py -r'
set -g status-left-length 45
set -g status-left '#[fg=colour3,bg=colour0,nobold] #(eval python ~/path/to/source/pomodoro.py)'
set -g status-interval 1
run-shell -b 'python pomodoro.py -r'
```
Use `<ctrl-leader><ctrl-r>` to reset the pomodoro
