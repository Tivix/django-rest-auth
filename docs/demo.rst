Demo project
============

To run demo project (ideally in virtualenv):

.. code-block:: python

    cd /tmp
    git clone git@github.com:Tivix/django-rest-auth.git
    cd django-rest-auth/demo/
    pip install -r requirements.pip
    python manage.py syncdb --settings=demo.settings --noinput
    python manage.py runserver --settings=demo.settings

Now, go to ``http://127.0.0.1:8000/`` in your browser.
