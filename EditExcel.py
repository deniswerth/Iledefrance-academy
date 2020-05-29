import xlwt, xlrd
import colorama



# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
RESET = colorama.Fore.RESET


class excel():
    
    def __init__(self, file_name, name, lab, research_group, tel, email, arxiv_page):
        """
        file_name : path + name of the file that is created
        name, lab, research_group, tel, email, arxiv_page : lists
        """
        self.name, self.lab, self.research_group, self.tel, self.email, self.arxiv_page = name, lab, research_group, tel, email, arxiv_page
        self.file_name = file_name


    def write_excel(self):
        """
        This function creates an excel file according to "path" and write the 
        information line by line according to "name", "lab", research_group",
        "tel", "email" and "arxiv_page". The function names the file as LAB.xlsx.
        """
        file_name = self.file_name
        name, lab, research_group, tel, email, arxiv_page = self.name, self.lab, self.research_group, self.tel, self.email, self.arxiv_page
        # create the Excel file
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("file")
        # print headers of each column
        worksheet.write(0, 0, 'Name')
        worksheet.write(0, 1, 'Lab')
        worksheet.write(0, 2, 'Research group')
        worksheet.write(0, 3, 'Tel')
        worksheet.write(0, 4, 'Email')
        worksheet.write(0, 5, 'ArXiv page')
        # check if "name", "lab", "research_group", "tel", "email" and "arxiv_page" have the same length
        if not (len(name) == len(lab) == len(research_group) == len(tel) == len(email) == len(arxiv_page)):
            raise ValueError(f'{RED}The lists do not have the same size.')
        # write information
        n = len(name)
        for i in range(0, n):
            worksheet.write(1 + i, 0, name[i])
            worksheet.write(1 + i, 1, lab[i])
            worksheet.write(1 + i, 2, research_group[i])
            worksheet.write(1 + i, 3, tel[i])
            worksheet.write(1 + i, 4, email[i])
            worksheet.write(1 + i, 5, arxiv_page[i])
        # save the file according to "file_name"
        workbook.save(file_name)
        print(f"{GREEN}Excel file completed.")
        print(f"{RESET}")

