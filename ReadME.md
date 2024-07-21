# Build
> pyinstaller manage.py --name=tournament_maker --copy-metadata django-bootstrap-v5 --add-data=C:\Users\liam\PycharmProjects\tournament_maker\templates:templates 

> .\dist\tournament_maker\tournament_maker.exe loaddata data.json 
> .\dist\tournament_maker\tournament_maker.exe createsuperuser
> .\dist\tournament_maker\tournament_maker.exe runserver --noreload 

## DUMPADATA with utf8
> python -Xutf8 manage.py dumpdata --format=json --all --indent 2 > data.json
