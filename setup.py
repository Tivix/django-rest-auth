#!/usr/bin/env python

import os
from setuptools import setup, find_packages


here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.rst'))
long_description = f.read().strip()
f.close()


setup(
    name='django-rest-auth',
    version='0.9.5',
    author='Sumit Chachra',
    author_email='chachra@tivix.com',
    url='http://github.com/Tivix/django-rest-auth',
    description='Create a set of REST API endpoints for Authentication and Registration',
    packages=find_packages(),
    long_description=long_description,
    keywords='django rest auth registration rest-framework django-registration api',
    zip_safe=False,
    install_requires=[
        'Django>=1.8.0',
        'djangorestframework>=3.1.3',
    ],
    extras_require={
        'with_social': ['django-allauth>=0.25.0'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development'
    ],
)
