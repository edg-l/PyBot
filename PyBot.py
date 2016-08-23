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
Made by: Ryozuki, timakro
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

def follow(logfile):
    send("say PyBot {} connected".format(version))
    logfile.seek(0,2) # Go to the end of the file
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue

        # get the command and it's args
        org_command = line[1 + line.find('!'):]
        arg_str = org_command.split(maxsplit=1)[-1]
        command = org_command.split()

        # get the name of the command caller
        try:
            command_a = re.search(r"^\[\d\d-\d\d-\d\d \d\d:\d\d:\d\d\]\[chat\]: (?P<id>\d+):(?P<chat>(-|)\d+):(?P<PlayerName>.{,15}): (?P<command>.+)$", line)
            name = command_a.group('PlayerName')
            id_user = command_a.group('id')
        except:
            pass

        # listen for commands
        if line.find("[chat]"):
            if command[0] == "help":
                print("{}: issued the command !{}".format(name, command[0]))
                send("say [{}] PyBot {} commands: !help, !calc <operation>, !time, !dice".format(name, version))
            if command[0] == "time":
                curtime = time.strftime("%H:%M:%S", time.localtime())
                print("{}: issued the command !{}".format(name, command[0]))
                send("say [{}] Current Server Time: {}".format(name, curtime))
            if command[0] == "dice":
                    number = random.randrange(0, 6)
                    print("{}: issued the command !{}".format(name, command[0]))
                    send("say [{}] Rolled the dice and got: {}".format(name, number))
            if command[0] == "calc":
                try:
                    result = repr(aeval(arg_str))
                except:
                    result = traceback.format_exc().rsplit('\n', 2)[1]
                # escape result
                result = result.replace("\\", "\\\\").replace("\"", "\"\\")
                print("{}: issued the command !{}  {}".format(name, command[0], arg_str))
                send("say [{}] Result: {}".format(name, result))


with open(logfilename, 'r') as logfile:
    print("PyBot {} connected".format(version))
    follow(logfile)
