from sys import argv
import numpy as np
import wave, struct, math

step = 2 ** (1.0/12.0)
base_tones = ['c', 'cis', 'd', 'es', 'e', 'f',
              'fis', 'g', 'gis', 'a', 'bes', 'b']

def merge_peaks(peaks, frate):

    merged_peaks = []

    start = peaks[0][0]
    end = peaks[1][0]
    curr_peaks = peaks[0][1]

    for i in range(len(peaks)):
        peak = peaks[i]
        next_peak = peak

        if i+1 < len(peaks):
            next_peak = peaks[i+1]

        if np.array_equal(peak[1], curr_peaks):
            end = next_peak[0]

        else:
            merged_peaks.append((start, end, curr_peaks))
            start = peak[0]
            end = next_peak[0]
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

        segment_peaks = {}
        p_start = None

        for j in range(0, len(amps)):
            if amps[j] >= (20 * chunk_avg):
                segment_peaks[j] = amps[j]

        top_peaks = []

        if len(segment_peaks) > 3:

            for _ in range(3):
                max_peak_idx = sorted(segment_peaks.items(), key=lambda kv: kv[1], reverse=True)[0][0]
                top_peaks.append(max_peak_idx)
                del segment_peaks[max_peak_idx]
                try:
                    del segment_peaks[max_peak_idx - 1]
                    del segment_peaks[max_peak_idx + 1]
                except KeyError:
                    pass

        else:
            top_peaks = list(segment_peaks.keys())

        peaks.append((i, sorted(top_peaks)))

        i += int(frate / 10)

    return peaks

def frame_to_time(frame, frate):
    return frame / frate

def get_octave_and_pitch(freq):

    octave_start = base_freq * math.pow(2, -9/12)

    if (freq >= octave_start) and (freq < 2*octave_start):
        octave = 0
    elif freq < octave_start:
        i = -1
        while freq < (octave_start * (2 ** i)):
            i -= 1
        octave = i
    else:
        i = 2
        while freq >= (octave_start * (2 ** i)):
            i += 1
        octave = i-1

    octave_start *= math.pow(2, octave)

    curr_tone = octave_start
    next_tone = octave_start * step

    for id in range(12):

        if freq >= curr_tone and freq < next_tone:
            id, cents, octave_change = compute_cents(curr_tone, next_tone, freq, id)

            if octave_change:
                return (octave + 1, id, cents)

            return (octave, id, cents)

        curr_tone = next_tone
        next_tone *= step


def compute_cents(lower, higher, freq, id):

    cent_step = (higher - lower) / 100.0
    midpoint = lower + (50 * cent_step)

    if abs(lower - freq) < (cent_step / 2):
        return (id, None, None)

    if freq <= midpoint:
        cents = (freq - lower) / cent_step
        return (id, int(round(cents)), None)
    else:
        cents = (higher - freq) / cent_step
        octave = None
        if id + 1 > 11:
            id = -1
            octave = 1
        return (id+1, int(round(cents)), octave)

def pitch_to_string(octave, id, cents):

    pitch = base_tones[id]

    if octave >= 0:
        pitch += abs(octave + 1) * "'"
    elif octave < -1:
        pitch = pitch[0].upper() + (pitch[1:] if len(pitch) >= 2 else "")
        pitch += abs(octave + 2) * ','

    if cents:
        if cents > 0:
            pitch += '+' + str(cents)
        elif cents < 0:
            pitch += '-' + str(abs(cents))
    else:
        pitch += '+0'

    return pitch

def filter_cluster(amps, cluster_start, cluster_end):
    if cluster_end - cluster_start == 1:
        return cluster_start

    cluster_max = cluster_start
    cluster_center = cluster_start + ((cluster_end - cluster_start) // 2)
    center_dist = abs(cluster_max - cluster_center)

    for i in range(cluster_start+1, cluster_end):
        if amps[i] > amps[cluster_max]:
            cluster_max = i
            center_dist = abs(cluster_max - cluster_center)
        elif amps[i] == amps[cluster_max]:
            if abs(i - cluster_center) < center_dist:
                cluster_max = i
                center_dist = abs(cluster_max - cluster_center)

    return cluster_max

if __name__ == '__main__':

    base_freq = float(argv[1])
    fname = argv[2]

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
            start_time = frame_to_time(m_peak[0], frate)
            end_time = frame_to_time(m_peak[1], frate)

            result = str(start_time) + '-' + str(end_time) + ' '

            for peak in m_peak[2]:
                result += pitch_to_string(*get_octave_and_pitch(peak)) + ' '

            print(result)

    else:
        print('no peaks')
