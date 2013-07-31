import mechanize
import cookielib
import urllib2
from collections import deque
from time import sleep

# puush.me said they would delete all files from their system that haven't
# been accessed in the past month.  this script automatically accesses all
# your puush files

# Put your email and password in these files
PASSWORD_FILE = "/Users/jessica/Dropbox/scripts/puush-password.txt"
EMAIL_FILE = "/Users/jessica/Dropbox/scripts/puush-email.txt"
ERR_LOG = "/Users/jessica/Dropbox/scripts/puush-err.txt"

## Rate limits:
# I think you can open 350 pages before it complains, but make the program
# pause every 170 pages to be safe
RATE_LIMIT = 170

# Number of pages that have been opened
numOpens = 0

# Logs an error message
err = open(ERR_LOG, "w")
def errlog(string):
    print string
    err.write(string + "\n")

# Opens a page
def openPage(link):
    global numOpens
    if (numOpens % RATE_LIMIT == RATE_LIMIT - 1):
        print "Rate limit exceeded ... pausing for 1 hour"
        sleep(3600)
    try:
        print "Trying to open " + link
        numOpens += 1
        br.open(link)
        print "Opened " + link
        sleep(2)
    except:
        errlog("Cannot open " + link + " ... pausing for 1 hour")
        sleep(3600)
        openPage(link)

# Gets links to public, private, and gallery
def getPools(br):
    return [link for link in br.links(url_regex = '\?pool=\d+')]

# Gets the pages on each pool
def getPagesForPool(br, pool):
    openPage(pool.url)
    poolurl = br.geturl()
    pages = []
    for i in range(1, int(getLastPageNum(br)) + 1):
        pages.append(poolurl + "&page=" + str(i))
    return pages

# Gets all pages
def getPages(br):
    pages = []
    for p in getPools(br):
        pages.extend(getPagesForPool(br, p))
    return pages


# Gets all the picture links on a page.
def getLinksOnPage(br, page):
    openPage(page)
    return [l.url for l in br.links(url_regex = 'puu')]

# Gets the number of the last page of pictures so we know when to stop.
def getLastPageNum(br):
    pages = br.links(url_regex = 'page=')
    q = deque(pages, maxlen = 2)
    assert (len(q) != 1)
    if (len(q) == 0): 
        # there is only one page of screenshots
        return 1
    else:
        # take the second to last link marked "page"
        q.pop()
        lastpage = q.pop()
        return lastpage.url.split('=')[-1]

with open(EMAIL_FILE, 'r') as e:
    email = e.readline().strip()
with open(PASSWORD_FILE, 'r') as p:
    password = p.readline().strip()

# Set up mock browser
br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')]


# Log into site
openPage("http://puush.me/login")
br.select_form(nr=0)
br.form["email"] = email
br.form["password"] = password
br.submit()

urls = []
for page in getPages(br):
    urls.extend(getLinksOnPage(br, page))

# Open all URLs
for l in urls:
    openPage(l)

err.close()
