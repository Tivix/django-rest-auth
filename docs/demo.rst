Demo project
============

This demo project shows how you can potentially use
dj-rest-auth app with jQuery on frontend.
To run this locally follow the steps below.

.. code-block:: python

    cd /tmp
    git clone https://github.com/jazzband/dj-rest-auth.git
    cd dj-rest-auth/demo/
    pip install -r requirements.pip
    python manage.py migrate --settings=demo.settings --noinput
    python manage.py runserver --settings=demo.settings


Now, go to ``http://127.0.0.1:8000/`` in your browser. There is also a
Single Page Application (SPA) in React within the ``demo/`` directory. To run this do:

.. code-block:: python

    cd react-spa/
    yarn # or npm install
    yarn run start


Now, go to ``https://localhost:3000`` in your browser to view it.
