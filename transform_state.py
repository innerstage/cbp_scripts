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
states_dict = us.states.mapping('fips', 'name')

n = 0

for df in df_gen:
    n += 1
    print("{}/58 | {:.2f}%\n".format(n, n/58*100))

    df["naics"] = df["naics"].astype(str).str.replace("-","")
    df["naics_len"] = df["naics"].str.len()
    df = df[df["naics_len"]==6]
    df = df.drop(columns=["empflag", "pums_code", "naics_len"])

    df["naics_name"] = df["naics"].map(naics_map)

    df["state"] = df["geoid"].str[7:9].astype(str).replace({"14": "66", "43": "72"})
    df["state"] = df["state"].astype(str).map(states_dict)
    df = df.rename(columns={"naics": "naics_code", "emp": "Total Employees", "ap": "Total Annual Payroll", "est": "Total Establishments"})

    df = df[["year", "geoid", "state", "naics_code", "naics_name", "Total Establishments", "Total Employees", "Total Annual Payroll"]]

    if n==1:
        df.to_csv("cbp_data_by_state.csv", quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
    else:
        df.to_csv("cbp_data_by_state.csv", header=False, quoting=csv.QUOTE_NONNUMERIC, mode="a", index=False)
