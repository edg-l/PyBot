#!/usr/bin/env python3
import traceback
import re
import math
import time
import random
from asteval import Interpreter

'''
Name: PyBot
Version: 1.0
Made by:
- Ryozuki: https://github.com/Ryozuki/
Thanks for helping:
- Wolf: https://github.com/abck
- timakro: https://github.com/timakro
Commands: !help, !calc <operation>, !time, !dice

TODO:
- More commands
- Json config
'''

version = 1.0

# config:
wait_time = 3
logfilename = '../autoexec_server.log'
fifofilename = '../ddnet.fifo'

aeval = Interpreter(max_time=0.1)


def send(msg):
    with open(fifofilename, 'w') as fifofile:
        fifofile.write(msg + "\n")
    time.sleep(wait_time)
    logfile.seek(0,2)


def send_say(msg: str):
    msg = msg.replace('\\', '\\\\')
    msg = msg.replace('"', '\\"')
    send("say \"" + msg + "\"")


def follow(logfile):
    send("say PyBot {} connected".format(version))
    logfile.seek(0, 2)  # Go to the end of the file
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue

        re_result = re.search(r"^\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\]\[chat\]: (?P<id>\d+):(?P<chat>(-|)\d+):(?P<PlayerName>.{,15}): (?P<command>.+)$", line)
        if re_result:
            name = re_result.group('PlayerName')
            id_user = re_result.group('id')
            command = re_result.group('command')
            arg_str = command.split(maxsplit=1)[-1]

            if command.startswith("!help"):
                print("{}: issued the command {}".format(name, command))
                send_say("[{}] PyBot {} commands: !help, !calc <operation>, !time, !dice".format(name, version))

            if command.startswith("!time"):
                curtime = time.strftime("%H:%M:%S", time.localtime())
                print("{}: issued the command {}".format(name, command))
                send_say("[{}] Current Server Time: {}".format(name, curtime))

            if command.startswith("!dice"):
                number = random.randrange(0, 6)
                print("{}: issued the command {}".format(name, command))
                send_say("[{}] Rolled the dice and got: {}".format(name, number))

            if command.startswith("!calc "):
                try:
                    result = repr(aeval(arg_str))
                except:
                    result = traceback.format_exc().rsplit('\n', 2)[1]

                print("{}: issued the command {}".format(name, command))
                send_say("[{}] Result: {}".format(name, result))


with open(logfilename, 'r') as logfile:
    print("PyBot {} connected".format(version))
    follow(logfile)
