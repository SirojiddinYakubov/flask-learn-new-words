if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

#echo "pwd ${PWD}"

pip install --upgrade pip && pip install -r /requirements.txt
echo "Successfully installed requirements.txt"

echo "Database migrations started"
#FLASK_APP=manage.py flask db upgrade -d ./alembic head
echo "Apply database migrations"

# Start server
echo "Starting server"
python manage.py
