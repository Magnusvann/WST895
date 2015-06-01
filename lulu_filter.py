import demo as d
import lulu
import numpy as np

def lulu_filter(noisy,sf):
    prev_smoothed = noisy
    pulses = lulu.decompose(img=noisy,quiet=False,operator='LU')
    smoothness_inc = 0.01
    pulse_len = len(pulses.keys())
    pulses
    i=2
    while 1-smoothness_inc > sf and i < pulse_len:
        lulu_smoothed, areas, area_count = lulu.reconstruct(dict((k, pulses[k]) for k in pulses.keys()[0:i]), noisy.shape)
        lulu_smoothed = noisy - lulu_smoothed
        smoothness_inc = np.var(lulu_smoothed)/np.var(prev_smoothed)
        prev_smoothed = lulu_smoothed
        i = i + 1
    return lulu_smoothed