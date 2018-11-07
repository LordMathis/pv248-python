from sys import argv
import numpy as np
import wave, struct, math

time = 1

if __name__ == '__main__':
    fname = argv[1]

    with wave.open(fname, 'rb') as wav:

        data_size = wav.getnframes()
        frate = wav.getframerate()
        nchannels = wav.getnchannels()

        data = wav.readframes(data_size)

    data = np.array(struct.unpack('{n}h'.format(n=data_size*nchannels), data))

    data_per_channel = [data[offset::nchannels] for offset in range(nchannels)]
    data_avg = [sum(e)/len(e) for e in zip(*data_per_channel)]

    chunk_size = time * frate

    peaks = []
    chunk_num = math.floor(data_size / chunk_size)
    for i in range(0, chunk_num):

        chunk = data_avg[i*chunk_size:i*chunk_size+chunk_size]
        amps = np.abs(np.fft.rfft(chunk))
        chunk_avg = np.mean(amps)

        for j in range(0, len(amps)):
            if amps[j] >= (20 * chunk_avg):
                peaks.append(j)
        i += chunk_size

    if len(peaks) > 0:
        print('low = {}, high = {}'.format(np.min(peaks), np.max(peaks)))
    else:
        print('no peaks')
