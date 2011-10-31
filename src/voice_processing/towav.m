words = {'begin', 'city', 'enough', 'line', 'ocean', 'page', 'press', 'reach', 'still'};
for i = 1:9
    word = words{i}
    mat_file = sprintf('/Users/heranyang/Research/deeplearn/data/Dropbox/word_spec/sp_rbm_%s_0-2/spec_generative_0_0.mat', word);
    dat = load(mat_file);
    spec = dat.data;
    spec(1:10,:) = 0;
    spec(100:129,:) = 0;
    wav = ispecgram(spec);
    nwav = wav/max(wav);
    wavwrite(nwav, 19500, sprintf('%s.wav', word));
end