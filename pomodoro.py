import argparse
import pickle
import os
import time


file_name = os.path.expanduser('~/.pomodoro.state')
focus_duration = 25
break_duration = 5
total_duration = focus_duration + break_duration


def reset_file():
    data = {
        'start': time.time()
    }
    f = open(file_name, 'w')
    pickle.dump(data, f)
    f.close()


def display_ticker():
    try:    
        f = open(file_name, 'rb')
        data = pickle.load(f)
        f.close()
    except:
        reset_file()

    elapsed = int(time.time() - data['start'])
    minutes = int(elapsed / 60) % total_duration

    if elapsed % 2:
        leader = '>'
    else:
        leader = ' '

    progress_bar = ('[' + 
                    '=' * min(minutes, focus_duration) +
                    (leader if minutes < focus_duration else '') +
                    ' ' * max(focus_duration - minutes - 1, 0) +
                    '|' +
                    '=' * max(minutes - focus_duration, 0) +
                    (leader if minutes >= focus_duration else '') +
                    ' ' * min(total_duration - minutes - 1, break_duration) +
                    ']')

    state = 'Focus' if minutes < focus_duration else 'Break'
    min_remaining = (focus_duration - minutes if minutes < focus_duration else
    total_duration - minutes) - 1
    sec_remaining = 60 - (int(elapsed) % 60)
    cycles = int(elapsed / 60 / total_duration)

    if (minutes == focus_duration) and (sec_remaining > 58):
        os.system('zenity --info --text="Time for a break!" --title="pomodoro"')

    print('{} {:02d}:{:02d} {} '.format(
        progress_bar, 
        min_remaining,
        sec_remaining,
        '|' * cycles))

  
parser = argparse.ArgumentParser()
parser.add_argument('-r', action='store_true')
args = parser.parse_args()

if args.r:
    reset_file()
else:
    display_ticker()
