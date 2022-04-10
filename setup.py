from setuptools import setup

setup(
    name='waffleiron',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pymongo',
        'config',
        'python-docx',
        'pandas',
        'numpy',
        'openpyxl',
    ],

)
