# Created & Maintained by Jack Bayliss, MIT license.
import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
with requests.Session() as s:
   
   headers = {
       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }

  #  Get proxies from the free proxy list.
   def get_proxies():
    print("Getting Proxies...")
    url = 'https://free-proxy-list.net/'
    try:
     response = requests.get(url)
     parser = fromstring(response.text)
     proxies = set()
     for i in parser.xpath('//tbody/tr')[:10]:
         if i.xpath('.//td[7][contains(text(),"yes")]'):
             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
             proxies.add(proxy)
     return proxies
    except requests.exceptions.RequestException as e:
     print("Failed to get proxies.. retrying")
     return get_proxies()

  # Get the specified URL.
   def get_url(url):
    prox = get_proxies()
    for proxy in prox:
     proxies = {
      "http": proxy,
      "https": proxy
    }
    try:
     print('Getting URL ' + url)
     print("IP:" + str(proxy))

     request = s.get(url,headers=headers,proxies=proxies)
     return request

    except requests.exceptions.RequestException as e:
     print('Failed getting URL- retrying')
     print("IP:" + str(proxy))

     return get_url(url)

  # Post to the specified URL
   def post_url(url,data):
    prox = get_proxies()
    for proxy in prox:
     proxies = {
      "http": proxy,
      "https": proxy
    }
    try:
     print('POSTING URL' + str(url))
     print("IP:" + str(proxy))

     request = s.post(url,data=data, headers=headers,proxies=proxies);
     return request
     
    except requests.exceptions.RequestException as e:
     print('Failed posting to URL- retrying')
     print("IP:" + str(proxy))

     return post_url(url)
   
   # Login using user details
   def login_mafia():
    #  The random tz, s, c fields are base64 encypted string, showing things screensize.
    # s : Screensize
    #  c : RGB information
    # l : locale
    # tsz : Timezone
    # p : plugins
    # m : Other plugin information? 

    login = {
         'username' : "email",
         'password' : "password",
         'action' : "login",
         'o' : "",
         'fpsrc' : 'front',
         'start1' : 'start1',
         'start3' : 'start3',
         'tz' : 'MA==',
         's' : 'MjU2MHgxMDgweDI0',
         'c' : 'cmdiKDI1NSwyNTUsMjU1KSxyZ2IoMjA0LDIwNCwyMDQpLHJnYigyNTUsMjU1LDI1NSkscmdiKDk5LDk5LDIwNikscmdiKDIyMSwyMjEsMjIxKSxyZ2IoMjIxLDIyMSwyMjEpLHJnYigxMzYsMTM2LDEzNikscmdiKDAsMCwwKSxyZ2IoMCwwLDApLHJnYigxMjgsMTI4LDEyOCkscmdiKDE4MSwyMTMsMjU1KSxyZ2IoMCwwLDApLHJnYigyNTUsMjU1LDI1NSkscmdiKDI1NSwyNTUsMjU1KSxyZ2IoMTI3LDEyNywxMjcpLHJnYigyNTEsMjUyLDE5NykscmdiKDAsMCwwKSxyZ2IoMjQ3LDI0NywyNDcpLHJnYigwLDAsMCkscmdiKDI1NSwyNTUsMjU1KSxyZ2IoMTAyLDEwMiwxMDIpLHJnYigxOTIsMTkyLDE5MikscmdiKDIyMSwyMjEsMjIxKSxyZ2IoMTkyLDE5MiwxOTIpLHJnYigxMzYsMTM2LDEzNikscmdiKDI1NSwyNTUsMjU1KSxyZ2IoMjA0LDIwNCwyMDQpLHJnYigwLDAsMCk=',
         'l' : 'ZW4tR0I=',
         'tzs' : 'RXVyb3BlL0xvbmRvbg==',
         'done' : 'eWVz',
         'p' : 'Q2hyb21lIFBERiBQbHVnaW4vaW50ZXJuYWwtcGRmLXZpZXdlcixDaHJvbWUgUERGIFZpZXdlci9taGpmYm1kZ2NmamJicGFlb2pvZm9ob2VmZ2llaGphaSxOYXRpdmUgQ2xpZW50L2ludGVybmFsLW5hY2wtcGx1Z2lu',
         'm' : 'YXBwbGljYXRpb24vcGRmLGFwcGxpY2F0aW9uL3gtZ29vZ2xlLWNocm9tZS1wZGYsYXBwbGljYXRpb24veC1uYWNsLGFwcGxpY2F0aW9uL3gtcG5hY2w=',
         'start2' : 'start2'
      }

    
    get_page = get_url("https://mafiareturns.com/")
    souped = BeautifulSoup(get_page.content, 'html.parser')



    pos = post_url("https://mafiareturns.com/login.php",login)
    soup = BeautifulSoup(pos.content, 'html.parser')
    try:
     name = soup.find("a", {"class": "eight"}).text
     if name=="Forename_Surname":
      return True
     else:
      return False
    except AttributeError as error:
     print("Error logging in, maybe banned?")
     return False
   
   # Return the drug prices.
   def getdrugprices():
    drugs = get_url("https://mafiareturns.com/profit/drugs.php")
    soup = BeautifulSoup(drugs.content.strip(),'html.parser')
    even = soup.findAll("tr",{"class":"even"})
    odd = soup.findAll("tr",{"class":"odd"})

    strings = []
    for data in even:
      strings.append(data.text.strip())
    for data in odd:
      strings.append(data.text.strip())

    return strings
   # Double check the IP address is different from original.
   def confirmip():
    proxy_ip = get_url("http://www.showmemyip.com/").content
    orig_ip = s.get("http://www.showmemyip.com/",headers=headers).content
    psoupy = BeautifulSoup(proxy_ip,"html.parser")
    osoupy = BeautifulSoup(orig_ip,"html.parser")
    orig_ip = osoupy.find("span",attrs={"class":"ipaddress"}).text
    proxy_ip = psoupy.find("span",attrs={"class":"ipaddress"}).text
    if(orig_ip!=proxy_ip):
     return True
    else: 
     print('IP ADDRESSES MATCH '+ orig_ip + ' ' +  proxy_ip)
     return False

   # Main method.
   def mafiareturns():
    if(confirmip()==True):
     login = login_mafia()
     if(login==True):
      drugs =  getdrugprices()
      for d in drugs: 
       print(d)
     else:
       print("Couldnt log in- you might be banned.")
    else:
     print("Your IP is visible, re running..")
     return os.execl(sys.executable, sys.executable, *sys.argv)

# Prints output
print(mafiareturns())