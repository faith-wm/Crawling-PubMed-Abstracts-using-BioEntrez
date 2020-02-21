
from Bio import Entrez
import csv
import pandas as pd
from Bio.Entrez import efetch
from Bio.Entrez import efetch, read
import argparse
import sys


##some parts of the code are copied from other sources --will paste the url of the source later- could not trace it at the moment

#i am using the Entrex library  details of the library can be found at https://biopython.org/DIST/docs/api/Bio.Entrez-module.html#esearch

def search(query,retstart=5,sort="pub+date", mindate="2010/01/01", maxdate="2019/9/27", retmax=100):       #define your desired date range, retmax= number of
                                                                        #documents to fetch each time
    Entrez.email = 'ffaith2010@gmail.com'                #input your email here
    handle = Entrez.esearch(db='pubmed',              #the esearch is a search function  #db specifies the Entrez databases name e.g., PubMEd
                            retmax=retmax,              # the details about the parameters can be found at  the url belpw
                            retmode='xml',      #https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
                            term=query,
                            retstart=retstart,
                            sort=sort,
                            mindate=mindate,
                            maxdate=maxdate)
    results = Entrez.read(handle)             #returns a list of pubmed articles ID- PMID, the length of the ids==retmax

    return results


#
# def fetch_details(id_list):                  #use efetch to fetch the returned  results
#     ids = ','.join(id_list)
#     Entrez.email = 'xxxxx'          #email
#     handle = Entrez.efetch(db='pubmed',
#                            retmode='xml',
#                            id=ids)
#     results = Entrez.read(handle)
#     return results
#
#
# def print_abstract(pmid):              #print sample abstracts by entering the article PMID
#     handle = efetch(db='pubmed', id=pmid, retmode='text',rettype='abstract')
#     #print(handle.read())
#     return 0





def get_abstract(pmid):         #returns a list of PMID- unique ids of pubmed articles, here i use the id to extract the article related to the id

    handle = efetch(db="pubmed", id=pmid,rettype="xml", retmode="text")
    xml_data = read(handle)#[0]

    # details of the efetch parameters can be found at https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch


    #from the xml data extract only articlews with abstract  and ignore the rest, there is many other information such as
    # author names,...but now am only interested in getting the document id (pmid), title and abstract if abstract is not available, return abstract=title

    abstracts = [pubmed_article['MedlineCitation']['Article']['Abstract']['AbstractText'][0] if 'Abstract' in
                pubmed_article['MedlineCitation']['Article'].keys() else pubmed_article['MedlineCitation']['Article']['ArticleTitle']
                 for pubmed_article in xml_data['PubmedArticle']]

    titles=[pubmed_article['MedlineCitation']['Article']['ArticleTitle'] for pubmed_article in xml_data['PubmedArticle']]

    titles_dict = dict(zip(pmid, titles))
    abstracts_dict = dict(zip(pmid, abstracts))

    #put the abstracts and titles to one dict with pmid as the key
    title_abstracts_dict = {key: [titles_dict[key], abstracts_dict[key]] for key in titles_dict}
    return title_abstracts_dict


def save_abstract(title_abstract_dict, saveFileName):       #function to save the extracted pmid, titles and abstracts
    with open(saveFileName, 'a') as outfile:                 # I use 'a' instead of 'w'
        writer = csv.writer(outfile)                           #'w' creates a new file but 'a' is for append so that even if the code breaks after
        for k, v in title_abstract_dict.items():                #resuming you just append new information without starting again
            writer.writerow([k] + v)


def fetched_abstract_len(savefilename, sep=","):             #fucntion to track the number of already fetched articles, it also helps in setting the retstart
                                                    #parameter for esearch function, #check the details of esearch to understand the usage of retstart
    try:
     file=pd.read_csv(savefilename, sep=sep)      #use try because in first iteration the savefilename does not exist yet
     return  len(file)
    except Exception:                              #if the file doesnt exist the len==0
        return 0





if __name__ == '__main__':
    # parser=argparse.ArgumentParser()
    # parser.add_argument('startdate',help='enter start date, the date you want to fetch articles from')
    # parser.add_argument('enddate',help='enter end date, the final date you want to fetch articles till')
    # parser.add_argument('saveFileName',help='enter the name for the file you want to save your results')
    # args=parser.parse_args()

    while True:
        savefilename='xxxx.csv'
        startdate='2010/01/01'
        enddate='2019/01/01'

        retstart = fetched_abstract_len(savefilename)
        results = search('internal medicine', retstart=retstart, mindate=startdate, maxdate=enddate)   #returns a list of PMID- unique ids of pubmed articles

        print("==> Fetched abstracts %d out of %s \n\n" %(retstart, results['Count']))   #i set the retmax to 100 in the search function, so each time 100 articles are fetched

        pmid_list = results['IdList']     #get list of PMID
        abstracts = get_abstract(pmid_list)   #use the PMID to get  the article information

        if len(pmid_list):
            abstracts=get_abstract(pmid_list)
            save_results=save_abstract(abstracts,savefilename)    #save the  extracted titles and abstract

        else:
            print("break")          #break if no more articles to fetch
            break




