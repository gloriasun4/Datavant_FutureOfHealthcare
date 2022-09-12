# -*- coding: utf-8 -*-
"""Datavant.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aTr1QM-Vn2GfX7FY7G6Pycw2gbDQT3Uy
"""

import pandas as pd
import numpy as np

df = pd.read_csv("drive/MyDrive/CMS_Inpatient.csv")
print(df.shape)
df.head()

noneed = ["DESYNPUF_ID", "CLM_ID", "SEGMENT", "CLM_FROM_DT", "CLM_THRU_DT", 
          "CLM_PMT_AMT", "NCH_PRMRY_PYR_CLM_PD_AMT", "AT_PHYSN_NPI", "OP_PHYSN_NPI", 
          "OT_PHYSN_NPI", "CLM_ADMSN_DT", "CLM_PASS_THRU_PER_DIEM_AMT", 
          "NCH_BENE_IP_DDCTBL_AMT", "NCH_BENE_PTA_COINSRNC_LBLTY_AM", 
          "NCH_BENE_BLOOD_DDCTBL_LBLTY_AM", "CLM_UTLZTN_DAY_CNT", "NCH_BENE_DSCHRG_DT"]
hcpcs = ["HCPCS_CD_" + str(i) for i in range(1, 46)]
noneed.extend(hcpcs)
df.drop(noneed, axis = 1, inplace = True)

dgns = ["ICD9_DGNS_CD_" + str(i) for i in range(1, 11)]
prcdr = ["ICD9_PRCDR_CD_" + str(i) for i in range(1, 7)]
# form_d = []
# for col in dgns:
#   form_d = np.hstack((form_d, df[col].unique()))
# form_p = []
# for col in prcdr:
#   form_p = np.hstack((form_p, df[col].unique()))
# form_d = np.unique(form_d)
# form_p = np.unique(form_p)

print(df.shape)
df.head()

provs = df.PRVDR_NUM.unique()

rng = np.random.default_rng()

rng.shuffle(provs)
states = np.array_split(provs, 50)

print(len(states))
print([len(each) for each in states])

dfs = []
for i in range(len(states)):
  df1 = df[df.PRVDR_NUM.isin(states[i])]
  dfs.append(df1)

print(len(dfs))

from collections import Counter

adms = []
clms = []
ic_dgns = []
ic_prcdr = []
for data in dfs:
  adm = data.ADMTNG_ICD9_DGNS_CD.value_counts().to_dict()
  adms.append(adm)
  clm = data.CLM_DRG_CD.value_counts().to_dict()
  clms.append(clm)
  # dgns = ["ICD9_DGNS_CD_" + str(i) for i in range(1, 11)]
  d = {}
  for each in dgns:
    dgns_val = data[each].value_counts().to_dict()
    newval = Counter(dgns_val)
    dd = Counter(d)
    dd.update(newval)
    d = dict(dd)
  ic_dgns.append(d)
  # prcdr = ["ICD9_PRCDR_CD_" + str(i) for i in range(1, 7)]
  dpr = {}
  for ea in prcdr:
    prcdr_val = data[ea].value_counts().to_dict()
    newval = Counter(prcdr_val)
    ddpr = Counter(dpr)
    ddpr.update(newval)
    dpr = dict(ddpr)
  ic_prcdr.append(dpr)

df_adm = pd.DataFrame.from_dict(adms)
df_clm = pd.DataFrame.from_dict(clms)
df_dgns = pd.DataFrame.from_dict(ic_dgns)
df_prcdr = pd.DataFrame.from_dict(ic_prcdr)

df_adm.fillna(0, inplace=True)
print(df_adm.shape)
df_adm.head()

df_clm.fillna(0, inplace=True)
print(df_clm.shape)
df_clm.head()

df_dgns.fillna(0, inplace=True)
print(df_dgns.shape)
df_dgns.head()

df_prcdr.fillna(0, inplace=True)
print(df_prcdr.shape)
df_prcdr.head()

options = [df_adm, df_clm, df_dgns, df_prcdr]

raw_options = []
for dfm in options:
  raw_options.append(list(dfm.columns))

fromdata = {}
for i in range(len(raw_options)):
  rng.shuffle(raw_options[i])
  categorize = np.array_split(raw_options[i], 10)
  fromdata[i] = categorize

print(len(list(fromdata.values())[0]))

# For example, we will be using the clm dataframe
all_categories_codes = fromdata.get(1)
cat_grouped = {}
for i in range(len(all_categories_codes)):
  cat_codes = all_categories_codes[i]
  cat_grouped[i] = options[1][cat_codes]

for i in range(len(cat_grouped.keys())):
  curdf = cat_grouped.get(i)
  summ = curdf.sum(axis=1).to_frame()
  summ.columns = ["Total"]
  curdf = pd.concat([curdf, summ], axis=1)
  cat_grouped[i] = curdf

cat_grouped.get(0).head()

mylist = []
for i in range(len(cat_grouped.keys())):
  mylist.append(cat_grouped.get(i).Total)
# state_freq = pd.concat(mylist, axis=1)
mydf = pd.DataFrame(mylist).T
# mydf.columns = ["cat_" + str(i) for i in range(len(cat_grouped.keys()))]
mydf.columns = ["Heart Disease", "Cancer", "Chronic Lower Respiratory Diseases", 
                "Cerebrovascular Disease", "Alzheimer's Disease", "Diabetes", 
                "Influence and Pnemonia", "Kidney Disease", "Mental Illness", 
                "Chronic Liver Disease"]
mydf["states"] = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
mydf

ax = mydf.plot(kind="bar", figsize=(30,8), title="Category Frequencies Across States", x="states")
ax.set_xlabel("States")
ax.set_ylabel("Frequency")
fig = ax.get_figure()
fig.savefig("categories_states.png")

# Functions that you could call to get the datas


# States_list: a list of states you want to compare
# Compare_cats: The categories you want to compare
# Returns: A figure with only the states and categories inputted
def compare_states(states_list, compare_cats):
  states_list = [state_idx.get(s) for s in states_list]
  compare_cats = np.append(compare_cats, ["states"])
  plot = mydf[compare_cats].iloc[states_list].plot(kind="bar", figsize=(30,8), title="Category Frequencies Across Selected States", x="states")
  plot.set_xlabel("States")
  plot.set_ylabel("Frequency")
  fig = plot.get_figure()
  fig.savefig("compare_states.png")


# Returns, in order of decreasing prevalence, the top k most prevalent categories in given state
def k_most_prevalent(k, my_state):
  my_state = state_idx.get(my_state)
  order = []
  for mycol in mydf.columns:
    if mycol == "states":
      continue
    order.append((mycol, mydf.loc[my_state, mycol]))
  order.sort(key = lambda x: x[1], reverse=True)
  return [c[0] for c in order[:k]]


# Finds the similarity score between two states, the lower means more similar.
def sim_score(state1, state2):
  if isinstance(state1, str):
    state1 = state_idx.get(state1)
  if isinstance(state2, str):
    state2 = state_idx.get(state2)
  sqdiff = 0
  for mycol in mydf.columns:
    if mycol == "states":
      continue
    sqdiff += (mydf.loc[state1, mycol] - mydf.loc[state2, mycol])**2
  return sqdiff

usstates = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
state_idx = {usstates[i]:i for i in range(len(usstates))}
# Finds the top k most similar states
def top_k_similar_states(k, my_state):
  my_state = state_idx.get(my_state)
  simscores = []
  for s in usstates:
    if state_idx.get(s) == my_state:
      continue
    hw = (s, sim_score(my_state, state_idx.get(s)))
    simscores.append(hw)
  simscores.sort(key=lambda x:x[1])
  return [s[0] for s in simscores[:k]]


# can then recommend to stock up on the appropriate meds/supplies, as applicable

# sample use
# choices = ["cat_" + str(i) for i in range(len(cat_grouped.keys()))]
choices = ["Heart Disease", "Cancer", "Chronic Lower Respiratory Diseases", 
                "Cerebrovascular Disease", "Alzheimer's Disease", "Diabetes", 
                "Influence and Pnemonia", "Kidney Disease", "Mental Illness", 
                "Chronic Liver Disease"]
wanted_fig = compare_states(rng.choice(usstates, size=rng.integers(1, high=50), replace=False), rng.choice(choices, size=10, replace=False))
print(k_most_prevalent(rng.integers(1, high=11), rng.choice(usstates)))
print(top_k_similar_states(rng.integers(1, high=50), rng.choice(usstates)))

# !pip -q install flask-ngrok

# !pip -q install pyngrok==4.1.1
# !ngrok authtoken 2EdmM1qZZJUGa5dDtZrPqQPjh9I_7QHSq7zGBcDLhkzHqDynv

# from flask import Flask
# from flask_ngrok import run_with_ngrok
# app = Flask(__name__)
# run_with_ngrok(app)   
  
# @app.route("/")
# def home():
#     return "<h1>Please help oh god</h1>"
    
# app.run()

