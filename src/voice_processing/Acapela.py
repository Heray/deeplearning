#!/usr/bin/env python
import httplib, urllib, urllib2, time
import re
import commands


def speakAcapela(word, speaker):

	speaker22k = speaker + '22k'
	params = urllib.urlencode({'client_login':'asTTS', 'client_password':'demo_web', 'client_request_type':'CREATE_REQUEST', 'client_voice':speaker22k, 'actionscript_version':'3','client_text':word})

	#headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Referer": "http://www.acapela-group.com/Flash/Demo_Web_AS3/demo_web.swf?path=http://vaas.acapela-group.com/Services/DemoWeb/&lang=EN", "Host":"vaas.acapela-group.com"}

	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

	#conn = httplib.HTTPConnection("www.acapela-group.com:80")
	conn = httplib.HTTPConnection("vaas.acapela-group.com:80")
	conn.request("POST", "/Services/DemoWeb/textToMP3.php", params, headers)
	response = conn.getresponse()
	print response.status, response.reason 
	data = response.read()

	print data

	#p = re.compile('http://[.]*.mp3')
	p = re.compile('http://.*mp3') #regular expression to parse out the mp3 url
	s = re.findall(p, data)[0] #mp3 url

	print s
	term_com = 'wget -q -U Mozilla -O %s_%s.mp3 %s' %(word, speaker, s)
	print commands.getstatusoutput(term_com)
	term_com = 'mpg123 -w %s_%s.wav %s_%s.mp3' % (word, speaker, word, speaker)
	print commands.getstatusoutput(term_com)

	conn.close()
