echo "--> dropping database..."
rm db.sqlite3
echo "--> creating database and migrating..."
python manage.py syncdb
echo "--> creating some preset models..."
python manage.py create_models
