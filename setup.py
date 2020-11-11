#!/usr/bin/env python

import os

from setuptools import find_packages, setup

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.md'))
long_description = f.read().strip()
f.close()


about = {}
with open('dj_rest_auth/__version__.py', 'r', encoding="utf8") as f:
    exec(f.read(), about)

setup(
    name='dj-rest-auth',
    version=about['__version__'],
    author='iMerica',
    author_email='imichael@pm.me',
    url='http://github.com/jazzband/dj-rest-auth',
    description='Authentication and Registration in Django Rest Framework',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django rest auth registration rest-framework django-registration api',
    zip_safe=False,
    install_requires=[
        'Django>=2.0,<3.1',
        'djangorestframework>=3.7.0',
    ],
    extras_require={
        'with_social': ['django-allauth>=0.40.0,<0.43.0'],
    },
    tests_require=[
        'unittest-xml-reporting>=3.0.2',
        'responses>=0.5.0',
        'django-allauth==0.40.0',
        'djangorestframework-simplejwt>=4.4.0 ',
        'coveralls>=1.11.1'
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    python_requires='>=3.5',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
