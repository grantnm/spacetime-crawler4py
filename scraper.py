import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup
import lxml

# openlab cmd prompt: cd cs121-assignment-2/spacetime-crawler4py
# cmd prompt: scp -r spacetime-crawler4py grantnm@openlab.ics.uci.edu:/home/grantnm/cs121-assignment2

def scraper(url, resp):
    print("Hey this URL made it to scraper: ", url)
    links = extract_next_links(url, resp)
    print("Hey these links made it out of extract_next_links: ", links)
    links = [urldefrag(link)[0] for link in links]

    #print(links)

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
    
    # Use beautiful soup to get the content of the page
    soup = BeautifulSoup(resp.url, "lxml")

    # Should extracting the content of the page (for tokenization and such) happen here or elsewhere?
    
    # List comprehension to compile all links found, using the href tag
    return [link.get('href') for link in soup.find_all("a")]

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    valid = re.compile('(.*ics\.uci\.edu.*|.*informatics\.uci\.edu.*|.*cs\.uci\.edu.*|.*stat\.uci\.edu.*)')

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            print("URL stopped here: ", parsed.hostname)
            return False
        if not valid.match(parsed.hostname):
            print("URL stopped here: ", parsed.hostname)
            return False
        print("URL got past first two checks:", parsed.hostname)
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
