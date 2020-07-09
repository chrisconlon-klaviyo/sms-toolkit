from setuptools import find_packages, setup


setup(
    name='sms-toolkit',
    version='1.0.4',
    description='A collection of tools to work with SMS messages.',
    long_description=open('README.rst').read(),
    author='Klaviyo',
    author_email='community@klaviyo.com',
    url='https://github.com/chrisconlon-klaviyo/sms-toolkit',
    license='MIT',
    packages=find_packages(),
    package_data={'': ['README.rst']},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)
