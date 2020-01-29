python3 /var/www/app/manage.py makemigrations
# echo "makemigrations done.." 
python3 /var/www/app/manage.py migrate
# echo "mirate done.."
# echo "going to runserver.."
python3 /var/www/app/manage.py runserver 0.0.0.0:8000