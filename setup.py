from setuptools import setup, find_packages
import pyprosegur

long_description = open('README.md').read()

setup(
    name='pyprosegur',
    version=pyprosegur.__version__,
    license='MIT License',
    url='https://github.com/dgomes/pyprosegur',
    author='Diogo Gomes',
    author_email='diogogomes@gmail.com',
    description='Unofficial Python library to interface with Prosegur Alarmes PT/ES.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'aiohttp',
        'click',
      ],
    entry_points='''
        [console_scripts]
        pyprosegur=pyprosegur.cli:prosegur
    ''',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
