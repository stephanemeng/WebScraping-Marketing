
# coding: utf-8

# In[55]:


from bs4 import BeautifulSoup
import requests
import sys 

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


# In[45]:


url = 'https://www.erome.com/explore'


# In[46]:


soup = BeautifulSoup(requests.get(url).text,'lxml')


# In[60]:


div_albums = soup.find_all("div",{"id":"albums"})

for tag in div_albums:
    a_tags = tag.find_all("a")
    
userpage_list = [x['href'] for x in a_tags]
print('Total number of pages: '+str(len(userpage_list)))
#Download videos from every page of userpage_list
video_link_src=[]
for (idx,url) in enumerate(userpage_list):
    temp_soup = BeautifulSoup(requests.get(url).text,'lxml')
    videos_list = temp_soup.find_all('video')
    video_link_src += ['https:'+x.find('source')['src'] for x in videos_list]
    sys.stdout.write("\r{0}%".format(round((float(idx)/len(userpage_list))*100)))
    sys.stdout.flush()
    
#Download Files in the Erome Videos Directory
print("Downloading Videos")
for (idx,video_url) in enumerate(video_link_src):
    download_file(video_url)
    sys.stdout.write("\r{0}%".format(round((float(idx)/len(video_link_src))*100)))
    sys.stdout.flush()

