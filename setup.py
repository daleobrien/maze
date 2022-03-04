from setuptools import setup, find_packages

__version__ = '3.0.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='maze',
    packages=find_packages(),
    include_package_data=True,
    scripts=('maze/maze',),
    version=__version__,
    description='Application that generates mazes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Dale O\'Brien',
    author_email='dale@do.id.au',
    url='https://github.com/daleobrien/maze',
    install_requires=(
        'reportlab',
        'mako',
        'docopt'
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ),
    python_requires='>=3.7'
)
