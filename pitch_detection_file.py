import commands
#import numpy as np
from math import *
#import matplotlib.pyplot as plt


def freq(s):
    cmd = "python pitch.py -i %s" % (s)
    output = commands.getoutput(cmd)
    data = map(float, output.split())
    data = dict(zip(*[iter(data)] * 2))
    return data


def midi(s):
    cmd = "python pitch.py -i %s" % (s)
    output = commands.getoutput(cmd)
    data = map(float, output.split())
    for i in xrange(1, len(data), 2):
        if data[i] != -1.0:
            X = int(round(log((data[i] / 440.0), 2) * 12 + 69))
            data[i] = X
    data = dict(zip(*[iter(data)] * 2))
    return data


def notes(s):
    chroma = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    cmd = "python pitch.py -i %s" % (s)
    output = commands.getoutput(cmd)
    data = map(float, output.split())
    for i in xrange(1, len(data), 2):
        if data[i] != -1.0:
            X = int(fmod(round(log((data[i] / 440.0), 2) * 12 + 69), 12))
            data[i] = chroma[X]
    data = dict(zip(*[iter(data)] * 2))
    return data


if __name__ == '__main__':
    X = midi('output.wav')
    print X
