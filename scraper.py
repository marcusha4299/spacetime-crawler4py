import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup


def scraper (url, resp):
    """
    #Code adapted from BeautifulSoup website: add website here.
    soup = BeautifulSoup(resp.content, 'html.parser')
    links=[]
    for link in soup.find_all('a'):
        href=link.get('href')
        if href is not None:
            links.append(href)
    links=[link for link in links if is_valid(link)]
    
    base_url = urlparse(url)
    links =[base_url.scheme + '://' + base_url.netloc + link if link.startswith('/') else link for link in links]
    return links
    """
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):

    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    """
    Conner added this part. 
    
    Gets the unfragmented url.
    unfragmentedurl = urldefrag(resp.url)[0]

    if is_valid(resp.url):
       if resp.status == 200:
        #Core of the body works.
        
        #Check to see if core of body is "empty". 
            #IF empty, skip.
            #Else go through it.
    
        else:
            error_message = resp.error
    """
    
   
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    #Jay added this part
    link_list = []
    unfragmentedurl = urldefrag(resp.url)[0]
    if is_valid(unfragmentedurl):
        if resp.status == 200:
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            for link in soup.find_all('a'):
                href=link.get('href')
                if href is not None:
                    link_list.append(href) 
        # else:
        #     error_message = resp.error
    return link_list

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #Checking if the domain names of the URL is consistent with the URLS set in config.ini. If not one of those, return False.
        if parsed.netloc not in set(["www.ics.uci.edu", "ics.uci.edu",
                                     "www.cs.uci.edu", "cs.uci.edu",
                                       "www.informatics.uci.edu", "informatics.uci.edu",
                                         "www.stat.uci.edu", "stat.uci.edu"]):
           return False

        #added new code here
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
#this is for test