from setuptools import setup

setup(
    name='waffleiron',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-PyMongo',
        'config',
        'python-docx',
        'pandas',
        'openpyxl',
    ],

)
