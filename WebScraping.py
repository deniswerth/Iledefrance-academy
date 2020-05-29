import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import colorama
import numpy as np
import string as string_package
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import time




# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN
RESET = colorama.Fore.RESET


class personal_webpage_information():


    def __init__(self, url):
        """
        url : personal webpage URL (string)
        browser_path : path to browser in the computer (string) in order
        to use selenium
        """
        self.url = url
        # delay for selenium loading page
        self.delay = 300 # seconds
        # request url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "lxml")


    def longest_string(self, liste):
        """
        Returns the longuest string in a liste and "" if 
        the liste is empty 
        """
        if len(liste) != 0:
            return max(liste, key=len)
        else:
            return ""


    def shortest_string(self, liste):
        """
   	    Returns the shortest string in a liste and "" if 
        the liste is empty 
        """
        if len(liste) != 0:
            return min(liste, key=len)
        else:
            return ""


    def is_valid(self, url):
        """
        Checks whether 'url' is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)


    def set_to_array(self, set):
        """
        Transforms a set type to an array type.
        """
        numpy_array = []
        for x in set:
            numpy_array.append(x)
        return np.asarray(numpy_array)


    def get_all_website_links(self):
        """
        Returns all URLs (internal and external) that is found on 'url' 
        in which it belongs to the same website.
        """
        url = self.url
        # Initialize the set of links (unique links)
        internal_urls = set()
        external_urls = set()
        # all URLs of 'url'
        urls = set()
        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            # join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not self.is_valid(href):
                # not a valid URL
                continue
            if href in internal_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                if href not in external_urls:
                    print(f"{GRAY}[!] External link: {href}{RESET}")
                    external_urls.add(href)
                continue
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
            urls.add(href)
            internal_urls.add(href)
        return self.set_to_array(internal_urls), self.set_to_array(external_urls)


    def link_header(self, url):
        """
        Returns all valid headers/names (and their respective urls) of a 
        page given its link as url string.
        """
        headers = []
        headers_urls = []
        soup = self.soup
        for header in soup.find_all("a"):
            header_string = header.get_text()
            if any(c.isalpha() for c in header_string): #Select strings containing at least one letter
                invalidcharacters= set(string_package.punctuation)
                if not any(char in invalidcharacters for char in header_string) or '-' in header_string: #Select Headers without special any character
                    if not header_string in headers: #Ignore Headers that already exist 
                        headers.append(header_string)
                        # get the respective url
                        href = header.attrs.get("href")
                        if href == "" or href is None:
                            # href empty tag
                            continue
                        # join the URL if it's relative (not absolute link)
                        href = urljoin(url, href)
                        parsed_href = urlparse(href)
                        # remove URL GET parameters, URL fragments, etc.
                        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                        if not self.is_valid(href):
                            # not a valid URL
                            continue
                        headers_urls.append(href)
        headers = np.asarray(headers)
        headers_urls = np.asarray(headers_urls)
        return headers, headers_urls


    def open_url(self, url):
        """
        Opens 'url' on the internet.
        """
        webbrowser.open(url)


    def go_to_other_page(self, url):
        """
        Selects manuelly a header on a page and returns its url
        starting from 'url'.
        """
        headers, headers_urls = self.link_header(url)
        # print the headers
        print(f"{GREEN}\n ### SELECT A HEADER### \n")
        for header in headers:
            print(f"{RESET}-- " + header)
        print("\n")
        # chose a header
        chosen_header = input()
        while not chosen_header in headers:
            print(f"{GREEN}\n ###HEADER DOES NOT EXIST### \n")
            chosen_header = input()
        chosen_header_index = np.where(headers == chosen_header)
        chosen_header_url = headers_urls[chosen_header_index]
        # open the header's link if wanted
        print(f"{GREEN}\n ###OPEN THE LINK ? (y/n)### \n")
        if input() == "y":
            self.open_url(chosen_header_url[0])
        return chosen_header_url[0]


    def navigate_website(self):
        """
        Virtually navigates through the website.
        """
        url = self.url
        print(f"{CYAN}\n###NAVIGATE### \n" + "###PRESS Ctrl C IN THE KERNAL TO EXIT### \n")
        url_page = self.go_to_other_page(url)
        while True:
            url_page = self.go_to_other_page(url_page)


    def find_arXiv_page(self, name):
        """
        Returns the arXiv page URL of 'name' if it
        contains at least one article and returns 
        None if the name has no article found.
        """
        # initialize the browser
        browser = webdriver.Firefox(executable_path = "/home/dwerth/Documents/Etudiants_Ambassadeurs/Selenium_package/geckodriver")
        browser.implicitly_wait(self.delay)
        try:
            # browse arXiv main page
            browser.get("https://arxiv.org/")
            # select the search bar
            searchBar = browser.find_element_by_name("query")
            # type the name
            searchBar.send_keys(name)
            # type ENTER
            searchBar.send_keys(Keys.ENTER)
            # wait until the page is loaded
            wait_execution = type(browser.find_element_by_id("abstracts-1"))
            # check if the page contains at least an article
            URL = browser.current_url
            html_code = str(urllib.request.urlopen(URL).read())
            if "produced no results." in html_code:
                URL = ""
            # close browser
            browser.close()
            return URL
        except Exception as e:
            print("Exception found", format(e))


    def find_emails(self):
        """
        Finds all emails on a webpage given its "url". 
        """
        url = self.url
        # initialize the browser
        browser = webdriver.Firefox(executable_path = "/home/dwerth/Documents/Etudiants_Ambassadeurs/Selenium_package/geckodriver")
        browser.implicitly_wait(self.delay)
        browser.get(url)
        # initialize the page source code
        doc = browser.page_source
        # replace weird email by a valid email
        doc = doc.replace(" -At- ", "@")
        doc = doc.replace("’at’ ", "@")
        doc = doc.replace("`at`", "@")
        doc = doc.replace("'at'", "@")
        doc = doc.replace("(arobase/at)", "@")
        doc = doc.replace(" [AT] ", "[AT]")
        doc = doc.replace("[AT]", "@")
        doc = doc.replace(" [at] ", "[at]")
        doc = doc.replace("[at]", "@")
        doc = doc.replace(" (at) ", "(at)")
        doc = doc.replace("(at)", "@")
        doc = doc.replace(" (AT) ", "(AT)")
        doc = doc.replace("(AT)", "@")
        doc = doc.replace(" (@) ", "(@)")
        doc = doc.replace("(@)", "@")
        doc = doc.replace(" [@] ", "[@]")
        doc = doc.replace("[@]", "@")
        doc = doc.replace(" (arobase) ", "(arobase)")
        doc = doc.replace("(arobase)", "@")
        doc = doc.replace(" [DOT] ", "[DOT]")
        doc = doc.replace("[DOT]", ".")
        doc = doc.replace(" [dot] ", "[dot]")
        doc = doc.replace("[dot]", ".")
        doc = doc.replace(" (dot) ", "(dot)")
        doc = doc.replace("(dot)", ".")
        doc = doc.replace(" (.) ", "(.)")
        doc = doc.replace("(.)", ".")
        doc = doc.replace(" [.] ", "[.]")
        doc = doc.replace("[.]", ".")
        # find all emails than fit with regression
        emails = re.findall(r"[\w\.-]+@[\w\.\-]+.[\w\.\-]", doc)
        # delete repeated elements
        emails = list(set(emails))
        browser.close()
        return np.asarray(emails)


    def find_tel(self):
        """
        Finds all telephone numbers on a webpage given its "url". 
        """
        try:
            telephone = re.findall(r"((?:[+]33|\([+]33\))?(?:\s|-|\.)?(?:\(\d\)\d|\d{2}|\d|\(\d\)|\d{3})?(?:\s|-|\.)?(?:\d{2}|\d{3})?(?:\s|-|\.)?\d{2}?(?:\s|-|\.)?\d{2}?(?:\s|-|\.)?\d{2})",str(self.soup))
            telephone.append('')
            tel = str(self.longest_string(telephone))
            # delete first character if it is a space
            if tel[0] == " ":
       	        tel = tel[1:]
            # add +33 (0) if the number starts with 1
            if tel[0] == "1":
                prefixe = "+33 (0)"
                tel = prefixe + tel
            return tel
        except:
            return ""


    def find_names_according_to_emails(self, emails):
        """
        Finds the names given their emails.
        """
        split_emails = []
        names = []
        name_emails = []
        # loop over the emails found on webpage to select string before "@"
        n = len(emails)
        for i in range(n):
            string = emails[i].split("@")[0]
            # select emails with "."
            if "." in string:
                split_emails.append(string.split("."))
            # select emails with invalid character except "."
            invalidcharacters= set(string_package.punctuation)
            if any(char in invalidcharacters for char in string) and not "." in string:
                split_emails.append(string)
            # select emails with one word ie without special character
            if not any(char in invalidcharacters for char in string):
                split_emails.append(string)
        # loop to find the name on the page
        for i in range(n):
            split_email = split_emails[i]
            # if two words divided by dot
            if type(split_email) == list and len(split_email) == 2:
                prenom = split_email[0].lower().capitalize()
                nom = split_email[1].upper()
                names.append([prenom, nom])
                name_emails.append(emails[i])
            # if one word without special character
            if type(split_email) == str and not any(char in invalidcharacters for char in string):
                names.append([split_email.upper()])
                name_emails.append(emails[i])
        split_emails = np.asarray(split_emails)
        return names, name_emails


    def find_names_and_emails_on_webpage(self):
        """
        Gives the names and corresponding emails found 
        on a webpage given its "url"
        """
        emails = self.find_emails()
        names, name_emails = self.find_names_according_to_emails(emails)
        return names, name_emails


    def find_single_name(self, guess_name):
        """
        Sorts the name given by the function find_emails
        according to a webpage (this function works when the email is 
        composed just with the last name).
        """
        children = list(self.soup.body.descendants)
        # list of names found on the website
        names_found = []
        # select the name if one word
        if len(guess_name) == 1:
            for k in range(len(children)):
                try:
                    # if the name is found in the Website
                    if guess_name[0].lower() in children[k].string.lower():
                        names_found.append(children[k].string)
                except:
                    continue
        # select the right names
        if len(guess_name) == 2:
            names_found.append(guess_name[0] + " " + guess_name[1])
        # delete elements containing invalid characters
        invalidcharacters= set(string_package.punctuation)
        for element in names_found:
            if any(char in invalidcharacters for char in element) or "." in element:
                names_found.remove(element)
        names_found = self.shortest_string(names_found)
        return names_found


    def find_name(self, guess_name_list):
        """
        Finds the name of the person according to its
        occurence in the website.
        This function uses find_single_name.
        """
        n = len(guess_name_list)
        historic = []
        for k in range(n):
            name_k = self.find_single_name(guess_name_list[k])
            historic.append(name_k)
        return self.shortest_string(historic), np.argmin(np.array(historic))


    def find_name_email_tel_arXiv_on_webpage(self):
        """
        Gives the names and corresponding emails found 
        on a webpage given its "url"
        """
        start_time = time.time()
        url = self.url
        #page = requests.get(url)
        #soup = BeautifulSoup(page.text, "lxml")
        print(f"{GREEN}\n###\nURL : " + str(url) + "\n###\n")
        print(f"{RESET}")
        try:
            # find tels on the webpage
            tels = self.find_tel()
            # guess the names and emails according to webapge (can be multiple)
            guess_names, guess_emails = self.find_names_and_emails_on_webpage()
            # if emails not found on webpage
            if guess_emails == []:
                raise Exception(f"{RED}No email found on this webpage!")
            name, index = self.find_name(guess_names)
            email = guess_emails[index]
            # give the arXiv page
            Arxiv = self.find_arXiv_page(name)
            # print information found
            print(f"{CYAN}name   : " + str(name))
            print(f"{CYAN}tels   : " + str(tels))
            print(f"{CYAN}email  : " + str(email))
            print(f"{CYAN}ArXiv  : " + str(Arxiv))
            print(f"{RESET}")
            # print execution time
            print(f"{GREEN}---   %s seconds ---  " % (time.time() - start_time))
            print(f"{RESET}")
            return name, tels, email, Arxiv
        except Exception as e:
            print("Exception found", format(e))
        



