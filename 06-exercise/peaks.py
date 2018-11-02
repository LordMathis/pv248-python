from sys import argv
import numpy as np
import wave, struct

if __name__ == '__main__':
    input = argv[1]

    wave_file = wave.open(input, 'r')

    nframes = wave_file.getnframes()
    nchannels = wave_file.getnchannels()

    sample_rate = wave_file.getframerate()
    sample_width = wave_file.getsampwidth()

    T = nframes / float(sample_rate)
    read_frames = wave_file.readframes(nframes)

    wave_file.close()

    data = struct.unpack("%dh" %  nchannels*nframes, read_frames)
    data_per_channel = [data[offset::nchannels] for offset in range(nchannels)]
    data = [sum(x)/len(x) for x in zip(*data_per_channel)]

    print(data)
