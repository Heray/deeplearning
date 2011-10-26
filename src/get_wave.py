import cPickle as C
import gzip
import numpy as N
import scipy.io.wavfile as W
import pylab as P

LIMIT = 1000
# 13000: (129, 133)
counter = 0
DOWN_SAMPLE = 10

# move the data to the center of LIMIT
# prereq: len(data) < LIMIT
def center_vect(data):
    offset = int((LIMIT - len(data)) / 2)
    ndata = N.zeros((LIMIT))
    ndata[offset:offset+len(data)] = data
    return ndata

def down_sample_vect(vect):
    nvect = []
    for i in xrange(len(vect)):
        if i % DOWN_SAMPLE == 0:
            nvect.append(vect[i])
    return nvect

def read_word(word):
    try:
        data = W.read('words/%s.wav' % word)
    except:
        return
    freq = int(data[0])  # 16,000
    if not freq == 16000:
        raise Exception('shit wrong freq')

    freq = freq / DOWN_SAMPLE
    wav_data = down_sample_vect(data[1])
    if len(wav_data) > LIMIT or len(wav_data) < LIMIT * 0.9:
        return

    data = (data[0], center_vect(wav_data))
    overlap_size = int(0.01 * freq)  # 10ms ==> 160
    Pxx, freqs, bins, im = P.specgram(x=data[1], NFFT = 256, Fs=freq, 
                                    noverlap=overlap_size)
    #P.plot(data[1])
    #import pdb; pdb.set_trace()
    print Pxx.shape
    
    # For now, cut the spectrogram to make it fit
    # TODO: should use PCA instead
    if not Pxx.shape == (129, 4):
        raise Exception('shape mismatched')

    global counter
    counter += 1
    print len(data[1])

    return (data[1], Pxx)

words = open('words/1-1000.txt').readlines()
spec_list = []
wav_list = []
for word in words[:]:
    word = word.replace('\n','')
    if len(word) < 2: continue

    res = read_word(word)

    if not res == None:
        (wav, Pxx) = res
        # Pxx = N.log(abs(Pxx)**2)
        spec_list.append(Pxx.flatten())
        wav_list.append(wav)

print 'samples size: %s' % counter
print 'done with words, writing to gzip...'

OUTPUT_WAV = True
OUTPUT_SPEC = False

import pdb; pdb.set_trace()

if OUTPUT_WAV:
    datafile = gzip.open('wav_data_%d.pkl.gz' % counter, 'w')
    nwav = N.array(wav_list)/2.0**16 + 0.5
    C.dump(nwav, datafile)
    datafile.close()

if OUTPUT_SPEC:
    datafile = gzip.open('spectrogram_data_%d.pkl.gz' % counter, 'w')
    C.dump(N.array(spec_list), datafile)
    datafile.close()

