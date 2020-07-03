import pandas as pd
import numpy as np
pd.options.display.max_rows=200


total_rows = 0
na_naics, na_state, na_both, na_total = 0, 0, 0, 0

chunksize = 1000000
N = sum(1 for row in open("cbp_data_by_msa.csv", "r")) // chunksize + 1
print("N = {:,}".format(N))

missing_naics = np.array([])

i = 0
for df in pd.read_csv("cbp_data_by_state.csv", chunksize=chunksize):

    i += 1
    print("{}/{} | {:.2f}%\n".format(i, N, i/N*100))

    total_rows += len(df)

    null_naics = df[(df["naics_name"].isnull()==True) & (df["state"].isnull()==False)]
    null_state = df[(df["naics_name"].isnull()==False) & (df["state"].isnull()==True)]
    null_both = df[(df["naics_name"].isnull()==True) & (df["state"].isnull()==True)]
    null_total = df[df.isnull()==True]

    na_naics += len(null_naics)
    na_state += len(null_state)
    na_both += len(null_both)
    na_total += len(null_naics) + len(null_state) + len(null_both)

    na_codes = df[df["naics_name"].isnull()==True]["naics_code"].unique()
    for e in na_codes:
        missing_naics = np.append(missing_naics, str(e))
    #print("len(na_codes) = {}".format(na_codes.size))
    #print("len(missing_naics) = {}\n".format(missing_naics.size))


print("Total Rows = {:,}".format(total_rows))
print("Total NA Rows = {:,} | {:.2f}%".format(na_total, na_total/total_rows*100))
print("NA Naics = {:,} | {:.2f}%".format(na_naics, na_naics/total_rows*100))
print("NA State = {:,} | {:.2f}%".format(na_state, na_state/total_rows*100))
print("NA Both = {:,} | {:.2f}%".format(na_both, na_both/total_rows*100))

missing_naics = np.unique(missing_naics)
print("len(missing_naics) w/o dups = {}\n".format(missing_naics.size))

#with open("missing_naics.txt", "w") as file:
#    for e in missing_naics:
#        string = '"'+str(e)+'": ,\n'
#        file.write(string)