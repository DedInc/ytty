from setuptools import setup, find_packages
from sys import platform, exit

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

if 'win' not in platform:
    print('Only for windows!')
    exit()

setup(
    name='ytty',
    version='1.0.1',
    author='Maehdakvan',
    author_email='visitanimation@google.com',
    description='Ytty - Powerful tool for parsing, downloading and uploading videos from youtube based on selenium.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DedInc/ytty',
    project_urls={
        'Bug Tracker': 'https://github.com/DedInc/ytty/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['vidspinner', 'pyperclip', 'undetected-chromedriver', 'requests'],
    python_requires='>=3.6'
)
