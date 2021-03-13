#%%
import re
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd
from tkinter import *
from tkinter import filedialog 
import time



ua = UserAgent()



def cleaning(input):
    cnt=0
    cleaned=[]
    for _ in input:
        cleaned.append(input[cnt].text.strip())
        cnt+=1
    return cleaned


def rename_dups(test):
    new=[]
    for item in test:
        if item in new:
            #new.append(item+"_")
            pass
        else:
            new.append(item)
    return new


# metode for å hente jobbannonsen fra finn.no
def request_url(url):
    # get contents
    header = {'User-Agent': ua.random}
    r=requests.get(url, headers=header)
    # convert to beautifulsoup object
    soup=bs(r.content,features="lxml")
    return soup

# metode for å hente ønskede felt fra annonsen
def get_content(soup):
    overskrifter=soup.select("dt")
    innhold=soup.select("dl dt + dd")
    overskrifter=cleaning(overskrifter)
    innhold=cleaning(innhold)
    overskrifter = rename_dups(overskrifter)
    return overskrifter,innhold


# metode for å lagre annonsen til dataframe
def scrape_ad(url):
    soup = request_url(url)
    overskrifter,innhold = get_content(soup)
    save_df=pd.DataFrame([overskrifter,innhold])
    save_df=clean_header(save_df)
    save_df=save_df[['Arbeidsgiver','Stillingstittel','Frist','Ansettelsesform','Sektor','Sted','Bransje','Stillingsfunksjon']]
    save_df.insert(1,"url",url)
    return save_df


# metode for å velge tekstfil og returnere liste med url-er
def chooseFile(): 
    root = Tk()
    root.withdraw()
    directory = filedialog.askopenfilename(filetypes=[("TXT", '*.txt')])
    # Change label contents 
    f = open(directory)
    koder_=f.read().split()
    koder=[]
    #print(koder)
    for kode in koder_:
        koder.append(kode)
    return koder



# metode som går gjennom finn-koder i txt fil og lagrer til dataframe.
def scraping(koder):
    df = pd.DataFrame()
    for kode in koder:
        try:
            time.sleep(.1)
            save_df=scrape_ad(kode)
            df=df.append(save_df)
        except:
            print(f"noe er galt med url: {kode}")

    print(df.head())
    df=reorder(df)
    return df


# metode for å sette øverste rad som header i dataframe
def clean_header(df):
    new_header = df.iloc[0]
    df=df[1:]
    df.columns=new_header
    return df


# metode for å omorganisere dataframe
def reorder(df):
    column_names=['Arbeidsgiver','Stillingstittel','Frist','Ansettelsesform','Sektor','Sted','Bransje','Stillingsfunksjon','url']
    df=df.reindex(columns=column_names)
    return df


# metode for å lagre til excel
def lagre_fil(df):
    print(df.head())
    if input("\nønsker du å lagre fila? (y/n): ") == 'y':
        name=input("\nskriv inn ønsket filnavn")+".xlsx"
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        cnt=1
        for col in df:
            worksheet.set_column(cnt,cnt, (len(col)+10))  # Width of columns B:D set to 30.
            cnt+=1
        writer.save()

    else:
        pass

    




def main():
    koder = chooseFile()
    testing=scraping(koder)
    #lagre_fil(testing)
    



if __name__=="__main__":
    main()
# %%
