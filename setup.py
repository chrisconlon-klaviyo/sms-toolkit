import os
from setuptools import find_packages, setup


setup(
    name='sms-toolkit',
    version='1.0.1',
    description='A collection of tools to work with SMS messages.',
    long_description=open('README.rst').read(),
    author='Klaviyo',
    author_email='community@klaviyo.com',
    url='https://github.com/chrisconlon-klaviyo/sms-toolkit',
    license='MIT',
    packages=find_packages(),
    package_data={'': ['README.rst']},
)
