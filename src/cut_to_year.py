import pandas as pd
import sys

def main():
	"""This saves time in development. There's no need to go trhough all the database."""

	year = int(sys.argv[1])
	dt = pd.Timestamp(year+1, 1, 1)

	data = pd.read_csv('WCA_export/WCA_export_Results_Ordered.tsv', sep='\t')
	data["date"] = data['date'].astype('datetime64[ns]')
	data[data["date"] < dt].to_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep='\t', encoding='utf-8', index=False)

if __name__ == "__main__":
	main()

