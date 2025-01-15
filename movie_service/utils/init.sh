#!/bin/bash
export PGPASSWORD=$POSTGRES_PASSWORD
echo "Applying init.sql..."
psql -U $POSTGRES_USER -h $POSTGRES_HOST -f "/movie_service/utils/init.sql"
alembic upgrade head
if [ "$DEBUG" == "1" ]; then
    export PGPASSWORD=$MOVIE_PASSWORD
    echo "Insert data into table..."
    psql -U $MOVIE_USER -d $MOVIE_DB -h $MOVIE_HOST -f "/movie_service/utils/test_data.sql"
fi
exec "$@"