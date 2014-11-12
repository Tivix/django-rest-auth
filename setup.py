#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


import os

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.rst'))
long_description = f.read().strip()
f.close()


setup(
    name='django-rest-auth',
    version='0.3.1',
    author='Sumit Chachra',
    author_email='chachra@tivix.com',
    url='http://github.com/Tivix/django-rest-auth',
    description='Create a set of REST API endpoints for Authentication and Registration',
    packages=find_packages(),
    long_description=long_description,
    keywords='django rest auth registration rest-framework django-registration api',
    zip_safe=False,
    install_requires=[
        'Django>=1.5.0',
        'djangorestframework>=2.3.13',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    # cmdclass={},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
