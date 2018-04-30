from setuptools import setup

setup(
    name='WRA A.P.P.',
    packages=['web', 'data_model'],
    include_package_data=True,
    install_requires=[
        'flask', 'sqlite3'
    ],
)
