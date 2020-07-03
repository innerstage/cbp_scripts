# CBP Single File Creation

1. Dumped table `cbp` from the DataUSA Monet DB.
2. The file `cbp_dump.csv` was compressed and downloaded to wrangle it.
3. The relevant columns were: Year, Geo ID, MSA Name, NAICS Code and Name, Total Establishments, Total Employees and Total Annual Payroll. The measures were available directly, but it was necessary to map the Geo ID to the MSA Name, and the NAICS Code to its Name.
4. Source for the NAICS Descriptions: https://www2.census.gov/programs-surveys/cbp/technical-documentation/reference/naics-descriptions/naics2017.txt
5. Source for the FIPS Crosswalk used to map Geo ID to MSA Name: https://data.nber.org/cbsa-msa-fips-ssa-county-crosswalk/2017/cbsatocountycrosswalk2017.csv
6. Since smaller industries are hidden at lower geographic levels due to privacy reasons, I created an extra file that only indicates State called `cbp_data_by_state.csv`.
7. The resulting file `cbp_data_by_msa.csv` has around 60% of NANs on the MSAs, because not all the FIPS codes have a MSA assigned, I checked that all the NaNs fall in this category here: https://www.dol.gov/owcp/regs/feeschedule/fee/Effective_May_16_2004_County_and_State_FIPS.htm, so those rows can be dropped at MSA level.
8. Both files show 110 NaN NAICS codes, so I manually created a dictionary for the missing entries, effectively reducing the NaN values from 68% to 61% on the MSAs file, and to 0% on the States file.
9. The dump was moved to Hercules along with the pipeline to process it there.