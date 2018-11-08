from sys import argv
import numpy as np
import wave, struct, math

def merge_peaks(peaks):

    merged_peaks = []

    start = peaks[0][0]
    end = peaks[0][0]
    curr_peaks = peaks[0][1]

    for peak in peaks:
        if np.array_equal(peak[1], curr_peaks):
            end = peak[0]
        else:
            merged_peaks.append((start, end, curr_peaks))
            start = peak[0]
            end = peak[0]
            curr_peaks = peak[1]

    merged_peaks.append((start, end, curr_peaks))
    return merged_peaks

def get_peaks(data_avg, frate):
    peaks = []

    i = 0;

    while (i + frate) <= len(data_avg):

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

    return peaks

def frame_to_time(frame, frate):
    return frame / frate

def freq_to_pitch(freqs):
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

    peaks = get_peaks(data_avg, frate)

    if len(peaks) > 0:
        merged_peaks = merge_peaks(peaks)

        for m_peak in merged_peaks:
            print(frame_to_time(m_peak[0], frate),
                  frame_to_time(m_peak[1], frate),
                  m_peak[2])
    else:
        print('no peaks')
