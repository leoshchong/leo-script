from setuptools import setup, find_packages
from pip._internal.req import parse_requirements
from leo import APP_VERSION

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='leo-cli',
    version=APP_VERSION,
    author='Leo Chong',
    author_email='leo.h.chong@bbc.co.uk',
    description='command line interface',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'leo=leo:leo',
        ]
    },
    install_requires=reqs
)
