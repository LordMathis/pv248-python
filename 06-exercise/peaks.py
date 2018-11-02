from sys import argv
import numpy as np
import wave, struct

if __name__ == '__main__':
    input = argv[1]

    waveFile = wave.open(input, 'r')

    length = waveFile.getnframes()
    channels = waveFile.getnchannels()
    framerate = waveFile.getframerate()

    for i in range(0,length):
        waveData = waveFile.readframes(1)
        data = struct.unpack("<h", waveData)
        print(int(data[0]))
