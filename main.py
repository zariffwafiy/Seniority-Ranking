'''
1) have dataset in dataframe, cleaned 
2) each rule will be one function 
3) main function will run through whole program, checking condition by passing through each function
4) get the seniority ranking
'''

'''
print("Seniority Ranking")

import os, numpy as np, pandas as pd, openpyxl, csv

#will get flawed because there are 2 sheets actually
file = pd.read_excel("Banking Bonds (as of 20230406).xlsx")
df = pd.DataFrame(file)
#print(df)

#clean data 
df = df.drop(columns=["SENIORITY_RANKING", "SECURED_FG","SENIORITY_RANKING_CLAUSE", "SENIORITY_RANKING_DESCRIPTION", "SECURITY_STATUS_CLAUSE", "SECURITY_DESCRIPTION", "SIMILARITY_OF_FACILITY_NAME_WITH_SENIORITY_RANKING_DESCRIPTION"])
df = df.assign(RULE_1 = pd.Series(dtype=int))
df = df.assign(RULE_2 = pd.Series(dtype=int))
df = df.assign(RULE_3 = pd.Series(dtype=int))
df = df.assign(SENIORITY_RANKING = pd.Series(dtype=str))

#check first rule
def check_rule_1():
    for index, row in df.iterrows():
        facility_name = row["FACILITY_NAME"]

        if "Additional Tier 1" in facility_name or "AT1" in facility_name:
            df.at[index, "RULE_1"] = 1
        else:
            df.at[index, "RULE_1"] = 0

#check second rule 
def check_rule_2():
    for index, row in df.iterrows():
        facility_name = row["FACILITY_NAME"]

        if any(keyword in facility_name for keyword in ["Tier 1", "Non Innovative Tier-1", "Innovative Tier-1", "NIT1", "IT1", "Hybrid Tier-1", "NIT-1", "IT-1"]):
            df.at[index, "RULE_2"] = 1
        else: 
            df.at[index, "RULE_2"] = 0

def check_rule_3():
    for index, row in df.iterrows():
        facility_name = row["FACILITY_NAME"]

        if any(keyword in facility_name for keyword in ["Tier 2", "T2"]):
            df.at[index, "RULE_3"] = 1
        else: 
            df.at[index, "RULE_3"] = 0

def main():
    for index, row in df.iterrows():
        check_rule_1()
        check_rule_2()
        check_rule_3()
        rule_1_value = row["RULE_1"]
        rule_2_value = row["RULE_2"]
        rule_3_value = row["RULE_3"]

        if rule_1_value == 1:
            df.at[index, "SENIORITY_RANKING"] = "Additional Tier 1 Capital"
        elif rule_1_value == 0 and rule_2_value == 1:
            df.at[index, "SENIORITY_RANKING"] = "Tier 1 Capital"
        elif rule_1_value == 0 and rule_2_value == 0 and rule_3_value == 1:
            df.at[index, "SENIORITY_RANKING"] = "Tier 2 Capital"
        else: 
            df.at[index, "SENIORITY_RANKING"] = "Undefined"

main()

'''
print("Seniority Ranking")

import pandas as pd 

#without explicit loops and utilizing vectorized operations

# Read the dataset into a DataFrame
print("Reading data..")
df = pd.read_excel("Banking Bonds (as of 20230406).xlsx")

# Clean data 
print("Cleaning data..")
df = df.drop(columns=["SENIORITY_RANKING", "SECURED_FG", "SENIORITY_RANKING_CLAUSE", "SENIORITY_RANKING_DESCRIPTION", "SECURITY_STATUS_CLAUSE", "SECURITY_DESCRIPTION", "SIMILARITY_OF_FACILITY_NAME_WITH_SENIORITY_RANKING_DESCRIPTION"])

# Set columns with respective rules
print("Setting up rules..")
df["RULE_1"] = df["FACILITY_NAME"].str.contains("Additional Tier 1|AT1", case=False).astype(int)
df["RULE_2"] = df["FACILITY_NAME"].str.contains("Tier 1|Non Innovative Tier-1|Innovative Tier-1|NIT1|IT1|Hybrid Tier-1|NIT-1|IT-1", case=False).astype(int)
df["RULE_3"] = df["FACILITY_NAME"].str.contains("Tier 2|T2", case=False).astype(int)
df["RULE_4"] = df["FACILITY_NAME"].str.contains("Tier Subordinated|Sub", case=False).astype(int)
df["RULE_5"] = df["BASEL_FG"].str.contains("Y", case = False).astype(int)

# Calculate the SENIORITY_RANKING based on rules
print("Applying rules..")
df["SENIORITY_RANKING"] = "Undefined"
df.loc[df["RULE_1"] == 1, "SENIORITY_RANKING"] = "Additional Tier 1 Capital"
df.loc[(df["RULE_1"] == 0) & (df["RULE_2"] == 1), "SENIORITY_RANKING"] = "Tier 1 Capital"
df.loc[(df["RULE_1"] == 0) & (df["RULE_2"] == 0) & (df["RULE_3"] == 1), "SENIORITY_RANKING"] = "Tier 2 Capital"
df.loc[(df["RULE_1"] == 0) & (df["RULE_2"] == 0) & (df["RULE_3"] == 0) & (df["RULE_4"] == 0), "SENIORITY_RANKING"] = "Senior"
df.loc[(df["RULE_1"] == 0) & (df["RULE_2"] == 0) & (df["RULE_3"] == 0) & (df["RULE_4"] == 1) & (df["RULE_5"] == 1), "SENIORITY_RANKING"] = "Tier 2 Capital"
df.loc[(df["RULE_1"] == 0) & (df["RULE_2"] == 0) & (df["RULE_3"] == 0) & (df["RULE_4"] == 1) & (df["RULE_5"] == 0), "SENIORITY_RANKING"] = "Subordinated"

filtered_df = df[df["SENIORITY_RANKING"] != "Undefined"]
print(filtered_df.head(5))
 

df.to_csv("output.csv", index=False)