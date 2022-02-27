from setuptools import setup, find_packages

setup(
    name='chainexplorer',
    version='0.0',
    packages=find_packages(exclude=['tests*']),
    license='none',
    description='Quickly retrieve and explore Bitcoin blocks',
    long_description=open('README.md').read(),
    install_requires=[],
    url='REPOSITORY_URL',
    author='AUTHOR_NAME',
    author_email='AUTHOR_EMAIL'
)
