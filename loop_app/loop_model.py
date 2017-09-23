import threading
import time
import sys
from getch import getch
from web import serve_forever


run = True
state = {
    "controlCharacter"  : False
}
streams = {}



class listener(threading.Thread):
    def __init__(self, stream, buffer_filler, freq = 0.5):
        self.input_stream=buffer_filler
        self.stream_name = stream
        self.freq = freq
        print "listener initialized"
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        print "master listener running"
        global run
        global streams
        while run:
            buffer = self.input_stream()
            if buffer:
                for listener in streams[self.stream_name]:
                    if buffer:
                        buffer=listener(buffer)
            time.sleep(self.freq)

def create_stream(name, loop_listener, freq = 0.5):
    global streams
    streams[name]=[]
    listener(name, loop_listener, freq)

def addEventListener(stream, func):
    streams[stream].append(func)
    print stream + " updated. Added " + func.__name__ + "."

def event_listener(stream):
    def faux_wrapper(l):
        def wrapper(*args, **kwargs):
            ch = args[0]
            global run
            global state
            if ch == "\x03":
                run = False
                state['exit'] = 0
                return None
            else:
                return l(*args, **kwargs)
        addEventListener(stream, wrapper)
        return wrapper
    return faux_wrapper


create_stream("keyboard", getch, freq = 0.01)
create_stream("8888", serve_forever, freq = 0.01)

@event_listener(stream="keyboard")
def g(ch):
    if ch == "g":
        print "you pressed g"
        return None
    return ch

@event_listener(stream="keyboard")
def f(ch):
    if ch == "f":
        print "you pressed f"
        return None
    return ch

@event_listener(stream="keyboard")
def a(ch):
    if ch == "a":
        print "you pressed a"
        return None
    return ch

@event_listener(stream="keyboard")
def arrows(k):
    global state
    k=repr(k)
    if "x1b" in k:
        state['controlCharacter'] = True
        return None
    elif ("[" in k) and state['controlCharacter']:
        state['controlCharacter'] = True
        return None
    elif state['controlCharacter']:
        state['controlCharacter'] = False
        if k=="'A'":
            print "up"
        elif k=="'B'":
            print "down"
        elif k=="'C'":
            print "right"
        elif k=="'D'":
            print "left"
        return None
    else:
        return k

@event_listener(stream="keyboard")
def others(ch):
    if ch not in ['a','f','g']:
        print ch
    return ch

def main():
    global run
    while run:
        l="break"
    print "ran"

if __name__ == '__main__':
    main()
    sys.exit(state['exit'])