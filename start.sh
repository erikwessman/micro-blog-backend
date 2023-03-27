if [[ "$VIRTUAL_ENV" != "" ]]
then
  flask --app main.py run
else
  echo "Activate venv before starting the backend:"
  echo ". venv/bin/activate"
fi
