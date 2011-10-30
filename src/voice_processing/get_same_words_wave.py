import cPickle as C
import gzip
import numpy as N
import scipy.io.wavfile as W
import pylab as P

import get_words_acapela as A

mac_training_voices = ['Alex', 'Princess', 'Junior', 'Agnes', 'Bruce', 'Fred', 'Kathy', 'Vicki', 'Ralph', 'Victoria']

voices = A.training_voices + mac_training_voices

LIMIT = 13000
# 13000: (129, 133)
counter = 0
DOWN_SAMPLE = 10
CUT_WHITE_LIMIT = 512

sizes = []

def cut_white(data):
    start = 0
    end = len(data)
    for i in xrange(len(data)):
        if data[i] > CUT_WHITE_LIMIT:
            start = i
            break
    for i in xrange(len(data)):
        if data[len(data)-i-1] > CUT_WHITE_LIMIT:
            end = len(data)-i
            break
    return data[start:end]

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

def read_word(word, speaker):
    try:
        data = W.read('/home/heray/Workspace/data/cut_training_voices/%s_%s_cut.wav' % (word, speaker))
    except:
        print 'File %s_%s.wav not found' % (word, speaker)
        return
    freq = int(data[0])  # 16,000
    if not freq == 22050:
        #raise Exception('shit wrong freq')
        print 'shit wrong freq %d' % freq

    # freq = freq / DOWN_SAMPLE
    # wav_data = down_sample_vect(data[1])
    wav_data = data[1]
    sizes.append(len(wav_data))
    '''
    if len(wav_data) > LIMIT or len(wav_data) < LIMIT * 0.9:
        print 'wave length %d wrong' % len(wav_data)
        return
    '''
    data = (data[0], center_vect(wav_data))
    overlap_size = int(0.01 * freq)  # 10ms ==> 160
    overlap_size = 160
    # import pdb; pdb.set_trace()
    Pxx, freqs, bins, im = P.specgram(x=data[1], NFFT = 256, Fs=freq, 
                                    noverlap=overlap_size)
    #import pdb; pdb.set_trace()
    P.clf()
    print Pxx.shape
    P.plot(data[1], 'b')
    P.savefig('%s_%s.png' % (word, speaker))
    P.clf()
    # For now, cut the spectrogram to make it fit
    # TODO: should use PCA instead
    # if not Pxx.shape == (129, 165):
    #    raise Exception('shape mismatched')

    global counter
    counter += 1
    print len(data[1])

    return (data[1], Pxx)


words = open('1-1000.txt').readlines()
spec_list = []
wav_list = []
right_len_words = []

''' Output new wav after cutting the white space
for word in words:
    word = word.replace('\n','')
    for speaker in voices:
        try:
            data = W.read('/home/heray/Workspace/data/training_voices/%s_%s.wav' % (word, speaker))
        except:
            continue
        wav_data = cut_white(data[1])
        W.write('%s_%s_cut.wav' % (word, speaker), 22050, wav_data)
'''

for word in words:
    word = word.replace('\n','')
    is_right_len = True
    # if len(word) < 2: continue
    for speaker in voices:
        try:
            data = W.read('/home/heray/Workspace/data/cut_training_voices/%s_%s_cut.wav' % (word, speaker))
        except:
            is_right_len = False
            break
        wav_data = data[1]
        if len(wav_data) > LIMIT or len(wav_data) < LIMIT * 0.7:
            is_right_len = False
            print 'word %s not right length %d' % (word, len(wav_data))
            break
    if is_right_len:
        right_len_words.append(word)

print len(right_len_words)
word_voices_list = {}

for word in right_len_words:
    print word
    word_voices = []
    # if len(word) < 2: continue
    for speaker in voices:
        res = read_word(word, speaker)

        if not res == None:
            (wav, Pxx) = res
            # Pxx = N.log(Pxx)
            NP = N.log(Pxx.flatten()+1)
            word_voices.append(wav)
            spec_list.append(NP)
            wav_list.append(wav)
        else:
            raise Exception('No speaker %s found for word %s' % (speaker,word))
    word_voices_list[word] = word_voices

print 'samples size: %s' % counter
print 'done with words, writing to gzip...'

# import pdb; pdb.set_trace()

OUTPUT_WAV = True
OUTPUT_SPEC = False

for word, word_voices in word_voices_list.items():
    datafile = gzip.open('wav_%s.pkl.gz' % word, 'w')
    nwav = N.array(word_voices)/(2.0**16) + 0.5
    C.dump(nwav, datafile)
    datafile.close()

if OUTPUT_WAV:
    datafile = gzip.open('wav_data_%d.pkl.gz' % counter, 'w')
    nwav = N.array(wav_list)/(2.0**16) + 0.5
    C.dump(nwav, datafile)
    datafile.close()

if OUTPUT_SPEC:
    datafile = gzip.open('spec_data_%d.pkl.gz' % counter, 'w')
    C.dump(N.array(spec_list), datafile)
    datafile.close()


