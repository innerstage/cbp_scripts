import pandas as pd
import us
import csv
pd.options.display.min_rows = 3000

# CHUNKS GENERATOR
names=["naics", "empflag", "emp", "ap", "est", "geoid", "year", "pums_code"]
df_gen = pd.read_csv("cbp_dump.csv", chunksize=1000000, names=names)

# NAICS CODES
naics_df = pd.read_excel("6-digit_2012_Codes.xls", skiprows=1)
naics_map = {str(code):name for (code,name) in zip(naics_df["Unnamed: 0"], naics_df["Unnamed: 1"])}

# FIPS CODES
msa_df = pd.read_csv("cbsatocountycrosswalk2017.csv")
msa_dict = {str(fips_county).zfill(5):msa_name for (fips_county, msa_name) in zip(msa_df["fipscounty"], msa_df["cbsaname"])}

n = 0


for df in df_gen:
    n += 1
    print("{}/58 | {:.2f}%\n".format(n, n/58*100))

    df["naics"] = df["naics"].astype(str).str.replace("-","")
    df["naics_len"] = df["naics"].str.len()
    df = df[df["naics_len"]==6]
    df = df.drop(columns=["empflag", "pums_code", "naics_len"])

    df["naics_name"] = df["naics"].map(naics_map)

    df["msa_len"] = df["geoid"].str[7:].astype(str).str.len()
    df = df[df["msa_len"]==5] 
    df["msa"] = df["geoid"].str[7:].astype(str).map(msa_dict)
    df = df.rename(columns={"naics": "naics_code", "emp": "Total Employees", "ap": "Total Annual Payroll", "est": "Total Establishments"})

    df = df[["year", "geoid", "msa", "naics_code", "naics_name", "Total Establishments", "Total Employees", "Total Annual Payroll"]]

    if n==1:
        df.to_csv("CBP_Data.csv", quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
    else:
        df.to_csv("CBP_Data.csv", header=False, quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
