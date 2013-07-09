import mechanize
import cookielib
import urllib2
from collections import deque

# puush.me said they would delete all files from their system that haven't
# been accessed in the past month.  this script automatically accesses all
# your puush files

# Put your email and password in these files
PASSWORD_FILE = "puush-password.txt"
EMAIL_FILE = "puush-email.txt"

# Adds all the picture links to a list of URLs.
def getLinksOnPage(br, page):
    br.open(page)
    for l in br.links(url_regex = 'view'): 
        urls.append(l.url)

# Gets the number of the last page of pictures so we know when to stop.
def getLastPageNum(br):
    pages = br.links(url_regex = '\?page=')
    q = deque(pages, maxlen = 2)
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
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Log into site
br.open("http://puush.me/login")
br.select_form(nr=0)
br.form["email"] = email
br.form["password"] = password
br.submit()

# Get names of all puush pages
pages = []
for i in range(1, int(getLastPageNum(br)) + 1):
    pages.append("http://puush.me/account?page=" + str(i))

# Get all picture URLs
urls = []
for page in pages:
    getLinksOnPage(br, page)

# Open all URLs
for l in urls:
    br.open(l)
    print br.geturl()
