
from Bio import Entrez
import csv ,sys ,re
import pandas as pd
from Bio.Entrez import efetch, read
from bs4 import BeautifulSoup



def search(query ,retstart=5 ,sort="pub+date", mindate="2010/01/01", maxdate="2020/7/30", retmax=100):
    Entrez.email = 'xxx.com'
    handle = Entrez.esearch(db='pubmed',
                            retmax=retmax,
                            retmode='xml',
                            term=query,
                            retstart=retstart,
                            sort=sort,
                            mindate=mindate,
                            maxdate=maxdate)
    search_results = Entrez.read(handle)

    pmid_list =search_results['IdList']
    pmid_count =search_results['Count']
    return pmid_list, pmid_count  # returns list of PMID



def fetch_document(pmid):
    handle = efetch(db='pubmed', id=pmid, retmode='text' ,rettype='xml'  )  # ,rettype='abstract')
    return handle.read()



def save_abstract(pmid_list, txt_files_folder ,xml_files_folder):

    count =0
    for id in pmid_list:
        count= count +1

        print("==> Fetched abstracts %d out of %s" % (count, len(pmid_list)))

        xml_document =fetch_document(id)

        parse_xmltext = BeautifulSoup(xml_document, 'xml')

        try:
            delete_copyright_info = parse_xmltext.find('CopyrightInformation').decompose()
        except:
            pass

        # get title and abstract
        try:
            title = parse_xmltext.find('ArticleTitle').text
        except:
            continue

        try:
            abstract = parse_xmltext.find('Abstract').text
            abstract = re.sub('\n', ' ', abstract)
        except:
            continue


        with open(txt_files_folder +'/' + str(id) + '.txt', 'w') as abstfile:
            abstfile.write(title)
            abstfile.write(abstract)

        file = open(xml_files_folder + '/' + str(id) + '.xml', 'w')
        file.write(xml_document)


    return 0

if __name__ == '__main__':
    while True:
        query = ''
        txt_files_folder=''
        xml_files_folder =''

        pmid_list, pmid_count = search(query=query)
        save_abstract(pmid_list, txt_files_folder,xml_files_folder)
