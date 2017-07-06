import re
import operator 
import json
from collections import Counter
from nltk.corpus import stopwords
import string
import vincent
import pandas
import tweepy
 
while True: 
	fname = 'python.json'

	emoticons_str = r"""
		(?:
			[:=;] # Eyes
			[oO\-]? # Nose (optional)
			[D\)\]\(\]/\\OpP] # Mouth
		)"""
 
	regex_str = [
		emoticons_str,
		r'<[^>]+>', # HTML tags
		r'(?:@[\w_]+)', # @-mentions
		r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
		r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
		r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
		r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
		r'(?:[\w_]+)', # other words
		r'(?:\S)' # anything else
	]
    
	tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
	emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
	def tokenize(s):
		return tokens_re.findall(s)
 
	def preprocess(s, lowercase=False):
		tokens = tokenize(s)
		if lowercase:
			tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
		return tokens

	punctuation = list(string.punctuation)
	stop = stopwords.words('english') + punctuation + ['rt','via','RT']

	dates_ITAvWAL = []

	with open(fname, 'r') as f:
		count_all=Counter()
		geo_data ={
				"type":"FeatureCollection",
				"features":[]
			}
		for line in f:
			try:
				tweet = json.loads(line)
				# Create a list with all the terms
				#terms_only = [term for term in preprocess(tweet['text']) 
				#if term not in stop and
				#not term.startswith(('#', '@'))]
				if tweet['coordinates']:
					#print("we are in new loop")
					geo_json_feature={
						"type": "Feature",
						"geometry":tweet['coordinates'],
						"properties":{
							"text": tweet['text'],
							"created_at": tweet["created_at"]
							}
						}
					#print("finished loop")
					geo_data['features'].append(geo_json_feature)
				#terms_only = [term for term in preprocess(tweet['text']) if term.startswith('#')]
				#if '#' in terms_only:
					#print("in loop")
					#dates_ITAvWAL.append(tweet["created_at"])
					#print("finished loop")
				# Update the counter
				#count_all.update(terms_only)
				#word_freq = count_all.most_common(20)
				#labels, freq = zip(*word_freq)
				#data = {'data': freq, 'x': labels}
				#bar = vincent.Bar(data, iter_idx='x')
				#bar.to_json('term_freq.json')
				# a list of "1" to count the hashtags
				#ones = [1]*len(dates_ITAvWAL)
				# the index of the series
				#idx = pandas.DatetimeIndex(dates_ITAvWAL)
				# the actual series (at series of 1s for the moment)
				#ITAvWAL = pandas.Series(ones, index=idx)
				#per_minute = ITAvWAL.resample('1Min', how='sum').fillna(0)
				#time_chart = vincent.Line(per_minute)
				#time_chart.axis_titles(x='Time', y='Freq')
				#time_chart.to_json('time_chart.json')
				
			except: pass
		# Print the first 5 most frequent words
		#print(count_all.most_common(5))
		#print(dates_ITAvWAL)
		#print(ones)
		#print(idx)
		#print(ITAvWAL)
		#print(per_minute)
	with open('geo_data.json', 'w') as fout:
		fout.write(json.dumps(geo_data, indent=4))
	print("the end")