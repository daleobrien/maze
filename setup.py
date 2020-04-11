from setuptools import setup, find_packages

__version__ = '2.0.0'

description = '''App that generates mazes'''

setup(
    name='maze',
    packages=find_packages(),
    scripts=('maze/maze',),
    version=__version__,
    description=description,
    author='Dale O\'Brien',
    author_email='dale@do.id.au',
    url='https://github.com/daleobrien/maze',
    install_requires=(
        'reportlab',
        'mako',
        'docopt',
        'rjsmin'
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7'
    )
)
