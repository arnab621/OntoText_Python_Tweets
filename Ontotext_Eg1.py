
# coding: utf-8

# In[ ]:

#Testing the endpoint for S4 Ontotext
# Reference -  http://docs.s4.ontotext.com/display/S4docs/Twitter+IE

import pandas as pd
import json
import requests
import matplotlib.pyplot as plt
#for ipython
get_ipython().magic(u'matplotlib inline')

key = '' # Register for a S4 account to get your key and scret for using the HTTP API services
secret = ''
endpointUrl = "https://text.s4.ontotext.com/v1"

req = requests.get(endpointUrl, auth=(key, secret))
print (req.content.decode('utf-8'), '\n')
 
print ('Request Code: {}\n'.format(req.status_code))
 
head = dict(req.headers)
print ('Headers: ')
for each in head:
    print (each.capitalize(), ": ", head[each])


# In[ ]:

df = pd.read_csv('#digitalbank_tweets.csv') #CSV file containing tweets. Downloaded using Tweepy.
df1=df
#df1=df[1:1000] # Testing for a sample
document = list(df1.Tweet_Text)
str1 = ', '.join(document) # combining all tweet text into a single document

#str1 = "Running is a good exercise. You need to exercise often."
endpoint = "https://text.s4.ontotext.com/v1" #service endpoint url
service = "/twitie" #name of the service 

# Prepare the data
annotationSelectorsArray = [":", "Original markups:"]
data = {
    "document": str1,
    "documentType": "text/plain",
    "annotationSelectors": annotationSelectorsArray
}
jsonData = json.dumps(data)

#Prepare the POST headers

headers = {
    'Accept': "application/json",
    'Content-type': "application/json",
    'Accept-Encoding': "gzip",
}


# In[ ]:

# Prepare and execute the request
req = requests.post(
    endpoint+service, headers=headers,
    data=jsonData, auth=(key, secret))


# In[ ]:

#print (req.content)


# In[ ]:

out=json.loads(req.content.decode('utf-8'))


# In[ ]:

out1=out[u'entities']


# In[ ]:

# Output - Extraction of Annotations - http://docs.s4.ontotext.com/display/S4docs/Text+Analytics

hashtags = [i[u'string'] for i in out1[u'Hashtag']]
hashtagsCount = [[x.encode('ascii', 'ignore'),hashtags.count(x)] for x in set(hashtags)] # count of unique hashtags
#UserID = [i[u'string'].encode('ascii', 'ignore') for i in out1[u'UserID']]
#UserIDCount = [[x.encode('ascii', 'ignore'), UserID.count(x)] for x in set(UserID)] # count of unique hashtags
#Users = [i[u'user'].encode('ascii', 'ignore') for i in out1[u'UserID']]
#URLs = [i[u'string'].encode('ascii', 'ignore') for i in out1[u'URL']]
#tokens and POS category http://cs.nyu.edu/grishman/jet/guide/PennPOS.html
Tokens = [[i[u'string'].encode('ascii', 'ignore'), i[u'category'].encode('ascii', 'ignore')] for i in out1[u'Token']]


# In[ ]:

hashtagsCountPD = pd.DataFrame(hashtagsCount,  columns=['HashTag', 'Count'])


# In[ ]:

hashtagsCountPD.Count.mean() #to know an approx cutoff


# In[ ]:

hashtagsCountGT2 =hashtagsCountPD[hashtagsCountPD.Count > 400].copy()


# In[ ]:

xlabels=list(hashtagsCountGT2.HashTag)
my_plot = hashtagsCountGT2.plot(kind='bar',legend=None,title="HashTag Frequency")
my_plot.set_xlabel("HashTag")
my_plot.set_ylabel("Count of Mention")
my_plot.set_xticklabels(xlabels)
#my_plot = hashtagsCountGT2.plot(kind='bar')


# In[ ]:

Tokens = [[i[u'string'].encode('ascii', 'ignore'), i[u'category'].encode('ascii', 'ignore')] for i in out1[u'Token']]
Tokens #with POS tags


# In[ ]:

outstring = str1.decode('utf-8').encode('ascii', 'ignore')


# In[ ]:

with open("Tweets_#DigitalBank.txt", "w") as text_file:
    text_file.write(outstring)


# In[ ]:

from wordcloud import WordCloud
wordcloud = WordCloud().generate(outstring)


# In[ ]:

plt.imshow(wordcloud)
plt.axis("off")
wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

