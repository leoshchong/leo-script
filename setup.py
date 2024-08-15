from setuptools import setup, find_packages
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='leo-cli',
    version='0.0.1',
    author='Leo Chong',
    author_email='leo.h.chong@bbc.co.uk',
    description='command line interface',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'leo=leo:cli',
        ]
    },
    install_requires=install_requires,
)
