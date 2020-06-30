import pandas as pd

total_rows = 0
na_naics, na_msa, na_both, na_total = 0, 0, 0, 0

n = 0
for df in pd.read_csv("cbp_data_by_msa.csv", chunksize=1000000):

    n += 1
    print("{}/14 | {:.2f}%\n".format(n, n/58*100))

    total_rows += len(df)

    null_naics = df[(df["naics_name"].isnull()==True) & (df["msa"].isnull()==False)]
    null_msa = df[(df["naics_name"].isnull()==False) & (df["msa"].isnull()==True)]
    null_both = df[(df["naics_name"].isnull()==True) & (df["msa"].isnull()==True)]
    null_total = df[df.isnull()==True]

    na_naics += len(null_naics)
    na_msa += len(null_msa)
    na_both += len(null_both)
    na_total += len(null_naics) + len(null_msa) + len(null_both)


print("Total Rows = {:,}".format(total_rows))
print("Total NA Rows = {:,} | {:.2f}%".format(na_total, na_total/total_rows*100))
print("NA Naics = {:,} | {:.2f}%".format(na_naics, na_naics/total_rows*100))
print("NA MSA = {:,} | {:.2f}%".format(na_msa, na_msa/total_rows*100))
print("NA Both = {:,} | {:.2f}%".format(na_both, na_both/total_rows*100))
