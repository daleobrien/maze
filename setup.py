from setuptools import setup

__version__ = '1.0'

description = '''App that generates mazes'''

setup(
    name='maze',
    scripts=['src/maze'],
    version=__version__,
    description=description,
    author='Dale O\'Brien',
    author_email='dale@do.id.au',
    url='https://github.com/daleobrien/maze',
    install_requires=[
        'reportlab'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
