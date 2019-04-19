import pandas as pd
import sys

def main():

	year = int(sys.argv[1])

	data = pd.read_csv('WCA_export/WCA_export_Results_Ordered.tsv', sep='\t')
	data[data["year"] <= year ].to_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep='\t', encoding='utf-8', index=False)

if __name__ == "__main__":
	main()

