Demo project
============

The idea of creating demo project was to show how you can potentially use
django-rest-auth app with jQuery on frontend.
Do these steps to make it running (ideally in virtualenv).

.. code-block:: python

    cd /tmp
    git clone https://github.com/Tivix/django-rest-auth.git
    cd django-rest-auth/demo/
    pip install -r requirements.pip
    python manage.py migrate --settings=demo.settings --noinput
    python manage.py runserver --settings=demo.settings

Now, go to ``http://127.0.0.1:8000/`` in your browser.
