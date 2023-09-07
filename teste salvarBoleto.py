import re
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from colorama import Fore, Back, Style

def validador(pdf_file, nameExtract, cont):
    ver: bool = True
    pdf_obj: PdfReader = PyPDF2.PdfReader(pdf_file)
    pdf_page = pdf_obj.pages[cont]
    text: str = pdf_page.extract_text()
    regex = nameExtract
    matches = re.search(regex, text)
    if matches:
        print(Fore.GREEN + "boleto {cont} validado com sucesso!".format(cont = cont+1))
        ver = True
    else:
        print(Fore.RED + "boleto {cont} com nome errado!".format(cont = cont+1))
        ver = False

    return ver

def nomeFormat(nameExtract):
    nameComplet: str = ""
    regex = r"^((\w)(\w+)(\s[^D])(\w+))|^((\w)(\w+)(\s)(D\w)(\s\w)(\w+))"
    matches = re.finditer(regex, nameExtract, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        if match.group(1):
            nameComplet: str = "".join(
                match.group(2) + match.group(3).lower() + match.group(4) + match.group(5).lower())
            print(nameComplet)
        if match.group(6):
            nameComplet: str = match.group(7) + match.group(8).lower() + match.group(9) + match.group(
                10).lower() + match.group(11) + match.group(12).lower()
            print(nameComplet)

    return nameComplet

def paginas_pdf(pdf_file, contWeek, pasta_saida):
    pdf_reader: PdfReader = PyPDF2.PdfReader(pdf_file)
    cont_Pages = len(pdf_reader.pages)
    regex = r"Pagador\n(\w+\s(D\w+\s\w+|[^D]\w+)).+CPF"
    nameExtract: str = ""
    nameComplet: str = ""
    for i in range (cont_Pages):
        pdf_page = pdf_reader.pages[i]
        text: str = pdf_page.extract_text()
        matches = re.finditer(regex, text, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.group())):
                #print(groupNum)
                if groupNum == 1:
                    nameExtract = ''.join(match.group(groupNum))
        if(validador(pdf_file, nameExtract, i)):
            nameComplet = nomeFormat(nameExtract)
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_page)
            nome_arquivo: str = "Boleto " + nameComplet + " " + contWeek + ".pdf"
            with open(pasta_saida + "/" + nome_arquivo, 'wb') as f:
                pdf_writer.write(f)
            print(Fore.GREEN + "Boleto {cont} foi salvo!".format(cont=i + 1))
        else:
            print(Fore.RED + "Boleto {cont} não foi salvo!".format(cont = i+1))

def main():
    root = tk.Tk()
    root.withdraw()
    pdf_file = filedialog.askopenfilename(title = "Selecionar arquivo PDF", filetypes = (("PDF files", "*.pdf"), ("all files", "*.*")))
    pasta_saida = filedialog.askdirectory(title = "Selecionar pasta de saída")
    print(pdf_file)
    contWeek: str = input("Insira a semana: ")
    paginas_pdf(pdf_file, contWeek, pasta_saida)

if __name__ == "__main__":
    main()
