import pandas as pd

total_rows = 0
na_naics, na_state, na_both, na_total = 0, 0, 0, 0

n = 0
for df in pd.read_csv("cbp_data_by_state.csv", chunksize=1000000):

    n += 1
    print("{}/14 | {:.2f}%\n".format(n, n/58*100))

    total_rows += len(df)

    null_naics = df[(df["naics_name"].isnull()==True) & (df["state"].isnull()==False)]
    null_state = df[(df["naics_name"].isnull()==False) & (df["state"].isnull()==True)]
    null_both = df[(df["naics_name"].isnull()==True) & (df["state"].isnull()==True)]
    null_total = df[df.isnull()==True]

    na_naics += len(null_naics)
    na_state += len(null_state)
    na_both += len(null_both)
    na_total += len(null_naics) + len(null_state) + len(null_both)

    print(df[df["state"].isnull()==True]["geoid"].str[7:9].value_counts(dropna=False))


print("Total Rows = {:,}".format(total_rows))
print("Total NA Rows = {:,} | {:.2f}%".format(na_total, na_total/total_rows*100))
print("NA Naics = {:,} | {:.2f}%".format(na_naics, na_naics/total_rows*100))
print("NA State = {:,} | {:.2f}%".format(na_state, na_state/total_rows*100))
print("NA Both = {:,} | {:.2f}%".format(na_both, na_both/total_rows*100))
