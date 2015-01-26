echo "--> dropping database..."
rm db.sqlite3
echo "--> creating database and migrating..."
./manage.py syncdb
echo "--> creating some preset models..."
./manage.py create_models