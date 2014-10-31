# coding: utf-8
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

version = __import__('duashttp').get_version()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
install_requires = ['django-filter>=0.8',
                    'djangorestframework>=2.4.3']
CLASSIFIERS = [
    'Environment :: Web Environment',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django'
]

setup(
    name='django-unity-asset-server-http-client',
    version=version,
    install_requires=install_requires,
    packages=find_packages(exclude=['requirements', 'tests']),
    include_package_data=True,
    license='MIT License',
    description='REST-api bases over unity asset server for some routines.',
    long_description=README,
    url='https://github.com/tarvitz/django-unity-asset-server-http-client',
    author='Tarvitz',
    author_email='tarvitz@blacklibrary.ru',
    classifiers=CLASSIFIERS,
    zip_safe=True,
    platforms=['OS Independent'],
    download_url=(
        'https://github.com/tarvitz/'
        'django-unity-asset-server-http-client/archive/v%(version)s.tar.gz' % {
            'version': version}
    )
)
