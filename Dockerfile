FROM alang/django
ENV DJANGO_APP=Subway 
COPY . /usr/django/app
ENV DJANGO_MANAGEMENT_ON_START='collectstatic --noinput';'migrate --noinput';'loaddata core/role.json'
RUN pip install -r /usr/django/app/requirements.txt
