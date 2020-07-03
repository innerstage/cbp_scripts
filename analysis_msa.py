import pandas as pd
import numpy as np

total_rows = 0
na_naics, na_msa, na_both, na_total = 0, 0, 0, 0

chunksize = 1000000
N = sum(1 for row in open("cbp_data_by_msa.csv", "r")) // chunksize + 1
print("N = {:,}".format(N))

missing_naics = np.array([])
missing_msas = np.array([])

i = 0
for df in pd.read_csv("cbp_data_by_msa.csv", chunksize=chunksize):
    i += 1
    print("{}/{} | {:.2f}%\n".format(i, N, i/N*100))

    total_rows += len(df)

    null_naics = df[(df["naics_name"].isnull()==True) & (df["msa"].isnull()==False)]
    null_msa = df[(df["naics_name"].isnull()==False) & (df["msa"].isnull()==True)]
    null_both = df[(df["naics_name"].isnull()==True) & (df["msa"].isnull()==True)]
    null_total = df[df.isnull()==True]

    na_naics += len(null_naics)
    na_msa += len(null_msa)
    na_both += len(null_both)
    na_total += len(null_naics) + len(null_msa) + len(null_both)

    na_naics_codes = df[df["naics_name"].isnull()==True]["naics_code"].unique()
    for e in na_naics_codes:
        missing_naics = np.append(missing_naics, str(e))
    #print("len(na_naics_codes) = {}".format(na_naics_codes.size))
    #print("len(missing_naics) = {}\n".format(missing_naics.size))
    na_msas_codes = df[df["msa"].isnull()==True]["geoid"].str[7:].unique()
    for e in na_msas_codes:
        missing_msas = np.append(missing_msas, str(e))
    #print("len(na_msas_codes) = {}".format(na_msas_codes.size))
    #print("len(missing_msas) = {}\n".format(missing_msas.size))


print("Total Rows = {:,}".format(total_rows))
print("Total NA Rows = {:,} | {:.2f}%".format(na_total, na_total/total_rows*100))
print("NA Naics = {:,} | {:.2f}%".format(na_naics, na_naics/total_rows*100))
print("NA MSA = {:,} | {:.2f}%".format(na_msa, na_msa/total_rows*100))
print("NA Both = {:,} | {:.2f}%".format(na_both, na_both/total_rows*100))

missing_naics = np.unique(missing_naics)
print("len(missing_naics) w/o dups = {}\n".format(missing_naics.size))

#with open("missing_naics_2.txt", "w") as file:
#    for e in missing_naics:
#        file.write(str(e)+"\n")

missing_msas = np.unique(missing_msas)
print("len(missing_msas) w/o dups = {}\n".format(missing_msas.size))

#with open("missing_msas.txt", "w") as file:
#    for e in missing_msas:
#        file.write(str(e)+"\n")