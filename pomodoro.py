import argparse
import os
import time


focus_duration = 25
break_duration = 5
total_duration = focus_duration + break_duration


def reset():
    start = time.time()
    os.popen('tmux setb -b pomodoro-timer {}'.format(start))
    set_last_messaged_displayed('focus')


def get_start_time():
    start = os.popen('tmux showb -b pomodoro-timer').read()
    if start == '':
        reset()
        return get_start_time()
    return float(start)


def get_last_messaged_displayed():
    last_message = os.popen('tmux showb -b pomodoro-last-message').read()
    return last_message


def set_last_messaged_displayed(message):
    os.popen('tmux setb -b pomodoro-last-message {}'.format(message))


def display_popup_message(message):
    os.system('tmux splitw -t 0 -l 9 "cowsay {} && read"'.format(message))


def display_ticker():
    start = get_start_time()
    sec_elapsed = int(time.time() - start)
    min_elapsed = int(sec_elapsed / 60) % total_duration
    sec_remaining = 60 - (sec_elapsed % 60)
    if min_elapsed < focus_duration:
        min_remaining = focus_duration - min_elapsed - 1
    else:
        min_remaining = total_duration - min_elapsed - 1
    if sec_remaining == 60:
        min_remaining += 1
        sec_remaining = 0

    cycles = int(sec_elapsed / 60 / total_duration)
    leader = '>' if sec_elapsed % 2 else ' '

    progress_bar = (
        '[' +
        '=' * min(min_elapsed, focus_duration) +
        (leader if min_elapsed < focus_duration else '') +
        ' ' * max(focus_duration - min_elapsed - 1, 0) +
        '|' +
        '=' * max(min_elapsed - focus_duration, 0) +
        (leader if min_elapsed >= focus_duration else '') +
        ' ' * min(total_duration - min_elapsed - 1, break_duration) +
        ']'
    )

    if (min_elapsed == focus_duration and
            get_last_messaged_displayed() != 'break'):
        display_popup_message('Time for a break!')
        set_last_messaged_displayed('break')
    if (min_elapsed == 0 and
            get_last_messaged_displayed() != 'focus'):
        set_last_messaged_displayed('focus')
        display_popup_message('Time to focus!')

    print('{} {:02d}:{:02d} {} '.format(
        progress_bar,
        min_remaining,
        sec_remaining,
        '|' * cycles))


parser = argparse.ArgumentParser()
parser.add_argument('-r', action='store_true')
args = parser.parse_args()

if args.r:
    reset()
else:
    display_ticker()
