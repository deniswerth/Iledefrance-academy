from WebScraping import personal_webpage_information
from EditExcel import excel


#Get information from a webpage
url = "Copy/paste a website url here"
pwi = personal_webpage_information(url = url)
name, tel, email, Arxiv = pwi.find_name_email_tel_arXiv_on_webpage()


#Lab
lab_name = "Lab name"
URL = []


#Research groups
research_group = []

if len(URL) != len(research_group):
	print("ERROR !")
	print(len(URL))
	print(len(research_group))


#Search information
names = []
lab = []
tels = []
emails = []
arxiv_pages = []


for i in range(len(URL)):
    url = URL[i]
    pwi = personal_webpage_information(url = url)
    name, tel, email, Arxiv = pwi.find_name_email_tel_arXiv_on_webpage()
    names.append(name)
    tels.append(tel)
    emails.append(email)
    lab.append(lab_name)
    arxiv_pages.append(Arxiv)


#Edit Excel
file_name = "Path (saving file location with .xml extension)"
e = excel(file_name = file_name, name = names, lab = lab, research_group = research_group, tel = tels, email = emails, arxiv_page = arxiv_pages)
e.write_excel()

