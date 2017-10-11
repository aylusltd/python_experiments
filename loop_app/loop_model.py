import threading
import time
import sys
from getch import getch
from web import serve_forever, close_socket


run = True
state = {
    "controlCharacter"  : False,
    "exit" : 0
}
streams = {}
master_listeners = []


class listener(threading.Thread):
    def __init__(self, stream, buffer_filler, freq = 0.5, destroy = None):
        if destroy is None:
            print stream + " has no destroy"
        else:
            print stream + " has destroy"
        self.input_stream=buffer_filler
        self.stream_name = stream
        self.freq = freq
        self.destroy = destroy
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
        for l in master_listeners:
            if l.destroy is not None:
                try:
                    l.destroy()
                except:
                    print "already dead"

def create_stream(name, loop_listener, freq = 0.5, destroy=None):
    global streams
    streams[name]=[]
    master_listeners.append(listener(name, loop_listener, freq, destroy=destroy))

def addEventListener(stream, func):
    streams[stream].append(func)
    print stream + " updated. Added " + func.__name__ + "."

def event_listener(stream, key=None):
    def faux_wrapper(l):
        def wrapper(*args, **kwargs):
            ch = args[0]
            global run
            global state
            if ch == "\x03":
                run = False
                state['exit'] = 0
                return None
            elif key is None or ch == key:
                return l(*args, **kwargs)
            else:
                return ch
        addEventListener(stream, wrapper)
        return wrapper
    return faux_wrapper



create_stream("keyboard", getch, freq = 0.01)
create_stream("8888", serve_forever, freq = 0.01, destroy=close_socket)

@event_listener(stream="keyboard", key="g")
def g(ch):
    print "you pressed g"

@event_listener(stream="keyboard", key="f")
def f(ch):
    print "you pressed f"

@event_listener(stream="keyboard", key="a")
def a(ch):
    print "you pressed a"

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