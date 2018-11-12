from sys import argv
import numpy as np
import wave, struct, math

def merge_peaks(peaks, frate):

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
        p_start = None

        for j in range(0, len(amps)):
            if amps[j] >= (20 * chunk_avg):
                if p_start is None:
                    p_start = j

            elif p_start is not None:
                segment_peaks.append(filter_cluster(amps, p_start, j))
                p_start = None

        top_peaks = np.sort(np.array(segment_peaks))[:3]

        peaks.append((i, top_peaks))

        i += int(frate / 10)

    return peaks

def frame_to_time(frame, frate):
    return frame / frate

def freq_to_pitch(freqs):
    pass

def filter_cluster(amps, cluster_start, cluster_end):
    if cluster_end - cluster_start == 1:
        return amps[cluster_start]

    cluster_max = cluster_start
    cluster_center = cluster_start + ((cluster_end - cluster_start) // 2)
    center_dist = abs(cluster_max - cluster_center)

    for i in range(cluster_start+1, cluster_end):
        if peak > amps[cluster_max]:
            cluster_max = i
            center_dist = abs(cluster_max - cluster_center)
        elif peak == cluster_max:
            if abs(i - cluster_center) < center_dist:
                cluster_max = i
                center_dist = abs(cluster_max - cluster_center)

    return cluster_max

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
        merged_peaks = merge_peaks(peaks, frate)

        for m_peak in merged_peaks:
            print(frame_to_time(m_peak[0], frate),
                  frame_to_time(m_peak[1], frate),
                  m_peak[2])
    else:
        print('no peaks')
