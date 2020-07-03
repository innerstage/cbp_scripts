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
naics_df = pd.read_csv("naics2017.csv")
naics_map = {code.replace("-","").replace("/",""):desc for (code,desc) in zip(naics_df["NAICS"], naics_df["DESCRIPTION"])}
naics_map = {**naics_map, **MISSING_NAICS}

# FIPS CODES
msa_df = pd.read_csv("cbsatocountycrosswalk2017.csv")
msa_dict = {str(fips_county).zfill(5):msa_name for (fips_county, msa_name) in zip(msa_df["fipscounty"], msa_df["cbsaname"])}

i = 0
for df in df_gen:
    i += 1
    print("{}/{} | {:.2f}%\n".format(i, N, i/N*100))

    df = df[["naics", "emp", "ap", "est", "geoid", "year"]]

    df["naics"] = df["naics"].astype(str).str.replace("-","").str.replace("/","")
    df["naics_len"] = df["naics"].str.len()
    df = df[df["naics_len"]==6]

    df["naics_name"] = df["naics"].map(naics_map)

    df["msa_len"] = df["geoid"].str[7:].astype(str).str.len()
    df = df[df["msa_len"]==5] 
    df["msa"] = df["geoid"].str[7:].astype(str).map(msa_dict)
    df = df.rename(columns={"naics": "naics_code", "emp": "Total Employees", "ap": "Total Annual Payroll", "est": "Total Establishments"})

    df = df[["year", "geoid", "msa", "naics_code", "naics_name", "Total Establishments", "Total Employees", "Total Annual Payroll"]]

    df = df.dropna() # DROPPING NANs HERE

    if i==1:
        df.to_csv("cbp_data_by_msa.csv", quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
    else:
        df.to_csv("cbp_data_by_msa.csv", header=False, quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
