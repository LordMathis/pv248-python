from sys import argv
import numpy as np
import wave, struct, math

def merge_peaks():
    pass


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

    peaks = []

    i = 0;

    while (i + frate) < len(data_avg):

        chunk = data_avg[i:i+frate]
        amps = np.abs(np.fft.rfft(chunk))
        chunk_avg = np.mean(amps)

        segment_peaks = []

        for j in range(0, len(amps)):
            if amps[j] >= (20 * chunk_avg):
                segment_peaks.append(j)

        top_peaks = np.sort(np.array(segment_peaks))[:3]

        peaks.append((i, top_peaks))

        i += int(frate / 10)

    if len(peaks) > 0:
        # print('low = {}, high = {}'.format(np.min(peaks), np.max(peaks)))
        print(peaks)
    else:
        print('no peaks')
