source .env
export PGPASSWORD=$DB_PASSWORD


psql --host $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME -f schema.sql