import pandas as pd
import us
import csv
from util import MISSING_NAICS


# CHUNKS GENERATOR
names = ["naics", "empflag", "emp_nf", "emp", "ap_nf", "ap", "est", 
         "n1_4", "n5_9", "n10_19", "n_20_49", "n50_99", "n100_249", "n250_499", "n500_999", "n1000",
         "geoid", "year", "pums_code"]

chunksize = 1000000
N = sum(1 for row in open("cbp_dump.csv", "r")) // chunksize + 1
print("N = {:,}".format(N))

df_gen = pd.read_csv("cbp_dump.csv", chunksize=chunksize, names=names)

# NAICS CODES
#naics_df = pd.read_excel("6-digit_2012_Codes.xls", skiprows=1)
#naics_map = {str(code):name for (code,name) in zip(naics_df["Unnamed: 0"], naics_df["Unnamed: 1"])}
naics_df = pd.read_csv("naics2017.csv")
naics_map = {code.replace("-","").replace("/",""):desc for (code,desc) in zip(naics_df["NAICS"], naics_df["DESCRIPTION"])}
naics_map = {**naics_map, **MISSING_NAICS}

# FIPS CODES
states_dict = us.states.mapping('fips', 'name')

i = 0

for df in df_gen:
    i += 1
    print("{}/{} | {:.2f}%\n".format(i, N, i/N*100))

    df = df[["naics", "emp", "ap", "est", "geoid", "year"]]

    df["naics"] = df["naics"].astype(str).str.replace("-","").str.replace("/","")
    df["naics_len"] = df["naics"].str.len()
    df = df[df["naics_len"]==6]

    df["naics_name"] = df["naics"].map(naics_map)

    df["state"] = df["geoid"].str[7:9].astype(str).replace({"14": "66", "43": "72"})
    df["state"] = df["state"].astype(str).map(states_dict)
    df = df.rename(columns={"naics": "naics_code", "emp": "Total Employees", "ap": "Total Annual Payroll", "est": "Total Establishments"})

    df = df[["year", "geoid", "state", "naics_code", "naics_name", "Total Establishments", "Total Employees", "Total Annual Payroll"]]

    if i==1:
        df.to_csv("cbp_data_by_state.csv", quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
    else:
        df.to_csv("cbp_data_by_state.csv", header=False, quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
