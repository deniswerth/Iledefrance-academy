[![Python](https://img.shields.io/badge/python-3.8.2-blue.svg)](https://python.org)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-orange.svg)](https://pypi.org/project/beautifulsoup4/)
[![Selenium](https://img.shields.io/badge/Selenium-3.141-green.svg)](https://pypi.org/project/selenium/)

# Iledefrance-academy


## Motivations
This repository has been developed in the context of [Trophées des étudiants-ambassadeurs de l'Île-de-France 2019-2020](https://www.iledefrance.fr/trophees-des-etudiants-ambassadeurs-de-lile-de-france-2019-2020). The île-de-France region organises this competition intended for students in exchange. The trophy rewards showcasing the richness of the île-de-France region. In this respect, this project aims at promoting French academic research by creating a website cataloguing useful research contacts. 

The website can be found here:

## Documentation

### `WebScraping.py`
This class gets the useful information (name, tel, email, ArXiv page) on a webpage given its url. A typical example of usage is:

```python
from WebScraping import personal_webpage_information
url = "Copy/paste a website url here"
pwi = personal_webpage_information(url = url)
name, tel, email, Arxiv = pwi.find_name_email_tel_arXiv_on_webpage()
```

### `EditExcel.py`
This class edits a Excel file in the format shown in 





