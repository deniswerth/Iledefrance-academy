[![Python](https://img.shields.io/badge/python-3.8.2-blue.svg)](https://python.org)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-orange.svg)](https://pypi.org/project/beautifulsoup4/)
[![Selenium](https://img.shields.io/badge/Selenium-3.141-green.svg)](https://pypi.org/project/selenium/)

# Iledefrance-academy


## Motivations
This repository has been developed in the context of [Trophées des étudiants-ambassadeurs de l'Île-de-France 2019-2020](https://www.iledefrance.fr/trophees-des-etudiants-ambassadeurs-de-lile-de-france-2019-2020). The île-de-France region organises this competition intended for students in exchange. The trophy rewards showcasing the richness of the île-de-France region. In this respect, this project aims at promoting French academic research by creating a website cataloguing useful research contacts. 

The website can be found here: http://iledefrance-academy.com/

## Documentation
### `WebScraping.py`

| Argument  | Description  | Example |
| ------------- |:-------------:|:-------------:|
| **url:** *string* | Webpage url | "http://www.lkb.upmc.fr/boseeinsteincondensates/beugnon/" |

This class gets the useful information (name, tel, email, ArXiv page) on a webpage given its url. A typical example of usage is:

```python
from WebScraping import personal_webpage_information
url = "Copy/paste a website url here"
pwi = personal_webpage_information(url = url)
name, tel, email, Arxiv = pwi.find_name_email_tel_arXiv_on_webpage()
```

### `EditExcel.py`

| Argument  | Description  | Example |
| ------------- |:-------------:|:-------------:|
| **file_name:** *string* | Path (saving file location with .xml extension) | "Document/file.xml" |
| **name:** *list* | Contact names | ("name1", "name2") |
| **lab:** *list* | Lab names | ("IPN_Orsay", "ENS") |
| **research_group:** *list* | Research groups | ("team1", "team2") |
| **tel:** *list* | Tel numbers | ("123", "456") |
| **email:** *list* | Email adresses | ("a@abc.com", "b@abc.com") |
| **arxiv_page:** *list* | ArXiv page urls | ("page1.com", "page2.com") |

This class edits a Excel file in the format shown in ![IPN_Orsay.xml](IPN_Orsay.xml). A typical example of usage is:

```python
from EditExcel import excel
names = ("name1", "name2")
labs = ("IPN_Orsay", "ENS")
research_groups = ("team1", "team2")
tels = ("123", "456")
emails = ("a@abc.com", "b@abc.com")
arxiv_pages = ("page1.com", "page2.com")
file_name = "Document/file.xml"
e = excel(file_name = file_name, name = names, lab = labs, research_group = research_groups, tel = tels, email = emails, arxiv_page = arxiv_pages)
e.write_excel()
```

### `__Main.py`
This file is the main code where all the classes are imported and used.




