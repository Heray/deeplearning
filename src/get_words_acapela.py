#!/usr/bin/env python
import Acapela
import threading

#speakers:
#American Spanish - rosa	Arabic - salma		Arabic - youssef
#Arabic - leila			Arabic - mehdi		Arabic - nizar
#Brazilian Portuguese - marcia	Canadian French- louise	Catalan - laia
#Czeck - eliska			Danish - mette		Danish - rasmus
#Dutch(BE) - jeroen		Dutch(Be) - sofie	Dutch(NL) - femke
#Dutch(NL) - max		English(Arabic) - nizar	English(Indian) - deepa
#English(UK) - graham		English(UK) - lucy	English(UK) - peter
#English(UK) - rachel		English(US) - heather	English(US) - kenny
#English(US) - laura		English(US) - nelly	English(US) - ryan
#English(US) - tracy		Finnish	    - sanna	French - alice
#French - antoine		French - bruno		French - claire
#French - julie			French - margaux	French(BE) - justine
#German - julia			German - klaus		German - sarah
#Greek - dimitris		Italian - chiara	Italian - fabiana
#Italian - vittorio		Norwegian - kari	Norwegian - olav
#Polish - ania			Portuguese - celia	Russian - alyona
#Spanish - antonio		Spanish - ines		Spanish - maria
#Swedish(FIN) samuel		Swedish - elin		Swedish - emma
#Swedish - erik			Turkish - ipek

us_english = ['laura', 'tracy', 'heather', 'nelly', 'kenny', 'ryan']
uk_english = ['graham', 'rachel', 'lucy', 'peter']

accents = ['rosa', 'salma', 'youssef', 'leila', 'mehdi', 'nizar', 'marcia', 'louise', 'laia', 'eliska', 'mette', 'rasmus', 'jeroen', 'sofie', 'femke', 'max', 'nizar', 'deepa',
           'sanna', 'alice', 'antoine', 'julie', 'julia', 'dimitris', 'vittorio', 'ania', 'antonio', 'samuel', 'erik', 'bruno', 'margaux', 'klaus', 'chiara', 'kari', 'celia', 'ines', 'elin', 'ipek', 'claire', 'justine', 'sarah', 'fabiana', 'olav', 'alyona', 'maria', 'emma']

training_voices = us_english + uk_english

words = open('1-1000.txt').readlines()

for w in words[500:]:
    w = w.replace('\n','')
    print w
    threads = []
    for voice in training_voices:
        t = threading.Thread(target=Acapela.speakAcapela, args=(w, voice,))
        # Acapela.speakAcapela(w, voice)
        t.start()
        threads.append(t)

        for t in threads:
            t.join()

