#a custom logger module for the bot, very basic but it gets the job done
import time

def debug(msg):
    logf=open("log.txt","a")
    localtime = time.asctime( time.localtime(time.time()) )
    logf.write(f"DEBUG - {msg} - {localtime}\n")
    logf.close()

def error(msg):
    logf=open("log.txt","a")
    localtime = time.asctime( time.localtime(time.time()) )
    logf.write(f"ERROR - {msg} - {localtime}\n")
    logf.close()

def warning(msg):
    logf=open("log.txt","a")
    localtime = time.asctime( time.localtime(time.time()) )
    logf.write(f"WARNING - {msg} - {localtime}\n")
    logf.close()

def critical(msg):
    logf=open("log.txt","a")
    localtime = time.asctime( time.localtime(time.time()) )
    logf.write(f"CRITICAL - {msg} - {localtime}\n")
    logf.close()
