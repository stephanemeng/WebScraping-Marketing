
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd 
import json
import re
import sys


# In[3]:


#Extract all SI Integrator ID on the website
list_integratorid = []
for i in range(1,15):
    #Loop through all the existing pages of the webpage
    
    url_main = "http://www.imrobotic.com/jcs/?page={0}".format(i)
    
    #Gather HTML Source Code and create data Pipeline
    data = requests.get(url_main).text
    soup = BeautifulSoup(data,'lxml')
    
    list_integratorid+= [e.find('a')['href'].split('/')[-2] for e in soup.find('ul','integratorUl').find_all('li')]
    
#Create blank list of dictionnaries, each dico contains information for on SI integrator
integrator_dico_list = []

#Collect System Integrator IDs that have no contact information for future reference
id_with_nocontactinfo = []

#Create url of contact page for each integrator id based on template
for id in list_integratorid:
    
    url2 = "http://store.imrobotic.com/integrator/{0}/contact".format(id)
    soup2 = BeautifulSoup(requests.get(url2).text,'lxml')
    
    #Based on the HTML Source code, collect the contact Javascript variable with a regular expression
    script = soup2.find_all('script',string=re.compile('var vue'))
    
    #Collect the JSON Array linked to the contact variable, then extract it as a dictionnary 
    
    print(id+' OK',end='\r')
    try:
        temp_dico = json.loads(re.search('\{(.*)"',script[0].text).group()+'}')
        integrator_dico_list +=[temp_dico]
    except AttributeError:
        id_with_nocontactinfo += [id]
        continue


# In[4]:


df = pd.DataFrame(integrator_dico_list)


# In[5]:


df

