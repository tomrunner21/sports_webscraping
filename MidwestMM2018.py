#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re

def MidwestMM():
    url = "https://www.sports-reference.com/cbb/postseason/2018-ncaa.html"
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    count  = 0
    Midwest = soup.find("div", id = "midwest")
    table = Midwest.find("div", class_= "team16") #finds the place where the 16 teams are held
    round1 = table.find("div", class_ = "round") #finds only the first round, since I only need the 16 teams from the beginning once
    schools = round1.find_all(href=re.compile("schools"))
    school_dict = dict()
    for row in schools: #creates a key and value for each of the 16 teams in the school dictionary
        school_name = row.getText()
#         or (" " in school_name == True) this isn't needed below, as the replace fn doesn't effect non "-" colleges
        if((school_name == "Penn")):
            new_school_name = "pennsylvania"
            school_dict[new_school_name] = school_name
            
        elif((school_name == "NC State")):
            new_school_name = "north-carolina-state"
            school_dict[new_school_name] = school_name
            
        elif((school_name == "TCU")):
            new_school_name = "texas-christian"
            school_dict[new_school_name] = school_name
            
        elif((school_name.islower() == False)):
            if(('.' in school_name)):
                new_school_name = school_name.replace(" ", "-")
                new_school_name2 = new_school_name.replace(".", "")
                new_school_name2 = new_school_name2.lower()
                school_dict[new_school_name2] = school_name
            else:
                new_school_name = school_name.replace(" ", "-")
                new_school_name = new_school_name.lower()
                school_dict[new_school_name] = school_name
        else:
            school_dict[school_name] = school_name


    return round1

MidwestMM()


# In[1]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

def getDfMM():
    school_set = MidwestMM()
    dfs = []
    final_df = pd.DataFrame()
    for school in school_set:
        url = "https://www.sports-reference.com/cbb/schools/" + school + "/2018-gamelogs.html"
        page = urlopen(url).read()
        soup = BeautifulSoup(page)
        count = 0
        pre_DF = dict()
#         school_set = data_table()
        table = soup.find("tbody")
#         featuresWanted = {'date_game','game_location','opp_id','game_season','pts','opp_pts'}
        featuresWanted = {'opp_id','game_result','pts','opp_pts', 'date_game'}
        rows = table.find_all('tr')
        
        for row in rows:
            if (row.find('th', {"scope": "row"}) != None):
                for f in featuresWanted:
                    cell = row.find("td", {"data-stat": f})
                    a = cell.text.strip().encode()
                    text = a.decode("utf-8")
                    if f in pre_DF:
                        pre_DF[f].append(text)
                    else:
                        pre_DF[f]=[text]
                        
        df = pd.DataFrame.from_dict(pre_DF)
        df["opp_id"]= df["opp_id"].apply(lambda row: (row.split("(")[0]).rstrip())
#         really need to fully understand the line above me! ^^^^
        df["school_name"] = school_set[school]
        df["school_name"] = df["school_name"].apply(removeNCAA)
        final_df=pd.concat([final_df,df])
        
    return final_df

def removeNCAA(x):
    if("NCAA" in x):
        return x[:-5]
    else:
        return x
    
def csvDumpMM():
    df = getDfMM()
    df.to_csv("MidwestMM2018.csv")
    
csvDumpMM()


# In[ ]:




