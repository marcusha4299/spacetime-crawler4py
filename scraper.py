import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup

#Dictionary containing words of ALL links Ex: the -> 200, information -> 321 etc...
global_words_dictionary = dict()
#Dictionary cointaining # of words for a link Ex: Ics.uci.edu -> 150 words ics.uci.edu/home -> 210 words.
global_linkNumWords_dictionary = dict()
#Dictionary containing all the ics subdomains and how many times they were called EX: vision.ics.uci.edu -> 10
global_icsLink_dictionary = dict()
#Set of global stopwords to avoid.
global_stopWords = {"a", "about", "above", "after", "again",
                "against", "all", "am", "an", "and",
                "any", "are", "aren't", "as", "at",
                "be", "because", "been", "before", "being",
                "below", "between", "both", "but", "by", "can't", "cannot",
                "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
                "doing", "don't", "down", "during", "each", "few", "for", "from",
                "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
                "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
                "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
                "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
                "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", 
                "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", 
                "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", 
                "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", 
                "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", 
                "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", 
                "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", 
                "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", 
                "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", 
                "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

def scraper (url, resp):
    """    
            #Add urls to a URL dictionary here
            for url in scraped_urls:
                if url not in self.urlDict:
                    self.urlDict[url] = 1
        

    """
       
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):

    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    link_list = []

    #Unfrag the url so that we don't run the same webpages (Gets rid of the #aaaa #bbbb etc.)
    unfragmentedurl = urldefrag(resp.url)[0]

    #Check to see if we already ran that url against the list of saved urls.


    if is_valid(unfragmentedurl):
        #Check that we haven't already ran that link (checks if its in the dictionary)
        # if unfragmentedurl not in global_linkNumWords_dictionary:
        # Check that the webpage returns an ok 200 response, anything else we ignore (skip).
        if resp.status == 200:
            #Credit given to the BeautifulSoup library. https://www.crummy.com/software/BeautifulSoup/bs4/doc/
            #Takes an HTML file and gives us the HTML data from it.
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            #Grabs the text within the URL
            text_string = soup.get_text()           
            #Gets rid of " 's " in words
            remove_apos_text_string = re.sub(r"'s", " ", text_string)
            #Gets rid of all "bad input" except for apostrophes (not 's)
            updated_text_string = re.sub("[^a-zA-Z']", " ", remove_apos_text_string)
            list_of_words = updated_text_string.split()

            #If the webpage has more than 99 words, we consider it having more than "little information" (run through it)
            #Additionally, if a webpage is very large (larger than 10 MB for our definition, must make an assumption of how many words that is)
            if len(list_of_words) > 99 and len(list_of_words) < 159000:
                lowerList_of_words = [eachIndex.lower() for eachIndex in list_of_words]
                #Add list of words to the dictionary
                for eachWord in lowerList_of_words:
                    #Check if the token is not in the stop words list or is greater than length 1 (useless info from 1 letter/num)
                    if (eachWord not in global_stopWords) and (len(eachWord) > 1):
                        #Check if the token is already in the dictionary.
                        if eachWord in global_words_dictionary:
                            #If it exists, update the value by 1
                            global_words_dictionary[eachWord] += 1
                        else:
                            #If it does not exist, create a new key to tokenize the word
                            global_words_dictionary[eachWord] = 1

                #After all the checks, add the URl to the dictionary of Links -> num words
                global_linkNumWords_dictionary[unfragmentedurl] = len(list_of_words)
                #Parses the url, useful for the ICS portion.
                urlResponse = urlparse(unfragmentedurl)
                #Deals with the portion of collecting ICS pages specifically for this assignment
                
                if ".ics.uci.edu" in urlResponse.netloc:
                    #Check if it already exists in the ICS dictionary
                    #If it exists, add to the key + 1
                    if (urlResponse.scheme + "://." + urlResponse.netloc) in global_icsLink_dictionary:
                        global_icsLink_dictionary[(urlResponse.scheme + "://." + urlResponse.netloc)] += 1
                    #If it doesn't exist, create one, and set the key value to 1
                    else:
                        global_icsLink_dictionary[(urlResponse.scheme + "://." + urlResponse.netloc)] = 1
                
                #Finds the links within the HTML document. Uses 'a' to find all the hyperlinks.
                for link in soup.find_all('a'):
                    #Makes the HTML link into a usable string.
                    href=link.get('href')
                    if href is not None:
                        unfragmentedLink = urldefrag(href)[0]
                        link_list.append(unfragmentedLink)
            


    #Returns a list of links to be parsed/crawled later.
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
        if (".ics.uci.edu" or ".cs.uci.edu" or ".informatics.uci.edu" or ".stat.uci.edu") not in parsed.netloc:
            return False


        if re.search(
            r"(/css/|/js/|/bmp/|/gif/|/jpe?g/|/ico/"
            + r"|/png/|/tiff?/|/mid/|/mp2/|/mp3/|/mp4/"
            + r"|/wav/|/avi/|/mov/|/mpeg/|/ram/|/m4v/|/mkv/|/ogg/|/ogv/|/pdf/|/odc/|/wp-content/|/ppsx/"
            + r"|/ps/|/eps/|/tex/|/ppt/|/pptx/|/doc/|/docx/|/xls/|/xlsx/|/names/|/jpg/|jpeg"
            + r"|/data/|/dat/|/exe/|/bz2/|/tar/|/msi/|/bin/|/7z/|/psd/|/dmg/|/iso/"
            + r"|/epub/|/dll/|/cnf/|/tgz/|/sha1/"
            + r"|/thmx/|/mso/|/arff/|/rtf/|/jar/|/csv/"
            + r"|/rm/|/smil/|/wmv/|/swf/|/wma/|/zip/|/rar/|/gz/)",
            parsed.path.lower()):
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|odc|wp-content|ppsx|jpg|jpeg"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
    
    # *.jpeg

    except TypeError:
        print ("TypeError for ", parsed)
        raise
#this is for test
#testing git
#testing git 2
