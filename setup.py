from setuptools import setup

setup(
    name='blacken_docs',
    description='Run `black` on python code blocks in documentation files',
    url='https://github.com/asottile/blacken-docs',
    version='0.2.0',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=['black>=18.6b0'],
    py_modules=['blacken_docs'],
    entry_points={'console_scripts': ['blacken-docs=blacken_docs:main']},
)
