#!/bin/bash

export_file="WCA_export.tsv.zip"
export_folder="WCA_export"
ordered_file="WCA_export/WCA_export_Results_Ordered.tsv"
download=false

# First we check if the file exists.
if [ -f $export_file ]; then
	one_week=$(date -d 'now - 7 days' +%s) # export older than 1 week is suggested to be replaced
	date_of_export=$(date -r "$export_file" +%s)
	
	if (( date_of_export <= one_week )); then # Here we check how old the export is.
		echo "$export_file is older than 7 days."
		rm $export_file;
		download=true;
	else
		echo "$export_file is up to date."
	fi
else
	download=true;
fi

if [ "$download" = true ]; then
	echo "Downloading the latest export."
	wget https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip
fi

if [ ! -f $export_file ]; then
	echo "There was an error while downloading.";
	exit;
else
	order=false;
	if [ ! -d "$export_folder" ] || [ "$download" = true ]; then
		echo "Extracting $export_file"
		unzip "$export_file" -d "$export_folder"
		
		order=true;
	fi
	
	if [ ! -f "$ordered_file" ] || [ "$order" = true ]; then
		echo "Sorting results..."
		python3 src/create_sorted_tsv_with_date.py
	fi
	
	# delete possible existing pages, except css
	for f in $(ls pages); do
		if [ "$f" != "styles.css" ]; then
			rm pages/$f
		fi
	done
	
	echo "Computing statistics..."
	for f in $(ls src |grep stat*); do
		echo $f
		python3 src/$f page=true
	done
	echo "Computing done."
	
	python3 src/index.py
	python3 src/about.py
	echo "Open pages/index.html for a complete view."
fi
