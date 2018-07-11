#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
from subprocess import PIPE, Popen
import time


def cmdline(command):
	"""
       Function take shell command and run it as subprocess then provide output of command
    """
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

## Main function to run threads for taking thread dump for java process
def thread_caller():
	"""
       Function to take thread Dump. This function call cmdline to find Java Process ID and Number of Threads running before taking ThreadDump
       Take ThreadDump based after every 20sec which can be change by giving different number
       use Cltr+C to break the threadDump loop

       change /java/ with path for your process

    """
	##threading call function after every 20sec
	threading.Timer(20.0, thread_caller).start()

	thread_count = cmdline("ps axlH | grep '/java/' | wc -l")

	thread_sub_count = ''.join(thread_count)

	java_thread = int(thread_sub_count.splitlines()[0])

	print("Java Thread Count is", java_thread)

	##Change this if you want to find out any other java process

	output = cmdline("pgrep -fl java | grep '/java/' | awk {'print $1'}")

	#print("output is ", output)

	sub_process = ''.join(output)

	java_process = sub_process.splitlines()[0]

	print("java process is ", java_process)

	##timeStamp to append in log file
	time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S')

	print("time stamp is ", time_stamp)

	##Condition to start ThreadDump whne thread Counts are greater then 1000 and smaller then 2000

	if java_thread > 1000 and java_thread < 2000:

		##Creating Thread Dump command
		thread_dump_command = """sudo /opt/jdk1.8/bin/jstack -l %s > /tmp/threadDump_%s_%s.out"""%(java_process, java_thread, time_stamp)

		print("Thread dump command is", thread_dump_command)

		##Running thread dump command
		os.system(thread_dump_command)

##Calling threadDump function
thread_caller()
