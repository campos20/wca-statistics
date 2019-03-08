#!/bin/bash

export_file="WCA_export.tsv.zip"
export_folder="WCA_export"
download=false

# First we check if the file exists.
if [ -f $export_file ]; then
	one_week=$(date -d 'now - 7 days' +%s) # export older than 1 week is suggested to be replaced
	date_of_export=$(date -r "$export_file" +%s)
	
	if (( date_of_export <= one_week )); then # Here we check how old the export is.
		read -p "$export_file is older than 7 days. Do you want me to remove to download again?" yn
		
		case $yn in
		    [Yy]* ) rm $export_file; download=true;; # If the export is too old, we remove it so we can download it again.
		    [Nn]* ) echo "OK, let's keep the old version then.";;
		    * ) echo "Please answer y/n. Terminating."; exit;;
		esac
	else
		echo "$export_file is up to date."
	fi
else
	read -p "$export_file not found. Do you want me to download it? (y/n) " yn

	case $yn in
        [Yy]* ) download=true;;
        [Nn]* ) echo "OK, terminating"; exit;;
        * ) echo "Please answer y/n. Terminating."; exit;;
    esac
fi

if [ "$download" = true ] ; then
	wget https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip
fi

if [ ! -f $export_file ]; then
	echo "There was an error while downloading.";
	exit;
else
	if [ ! -d "$export_folder" ]; then
		echo "Extracting $export_file"
		unzip "$export_file" -d "$export_folder"
	fi
	
	# delete possible existing pages
	for f in $(ls pages); do
		if [ "$f" != "styles.css" ]; then
			rm pages/$f
		fi
	done
	
	echo "Computing statistics..."
	for f in $(ls src |grep stat*); do
		echo $f
		python3 src/$f
	done
	echo "Computing done."
	
	python3 src/build_main_page.py
fi
