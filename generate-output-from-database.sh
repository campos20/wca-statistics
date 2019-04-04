if ! sudo bash -c '[[ -d "/var/lib/mysql/WCA" ]]'
then
	echo "Building the database. This will take a while"
	sudo mysql -e "CREATE DATABASE WCA; USE WCA; SOURCE wca-developer-database-dump.sql;"
	echo "Finally done."
fi

# Create the temp
if [ ! -d database_out ]; then
    mkdir database_out
fi


# Generate output for the Statistics


# CountryName NumberOfDelegates
sudo mysql --disable-column-names -e "USE WCA; SELECT Countries.id, COUNT(Countries.name) FROM users JOIN Countries WHERE users.country_iso2 = Countries.iso2 AND users.delegate_status IS NOT NULL GROUP BY Countries.id;" > database_out/stat-database-ratio_delegates_competitors_last_year.txt
