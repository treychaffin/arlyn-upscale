"""Install parameters for CLI and python import."""
from setuptools import find_packages, setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name="arlyn",
    version="0.0.2",
    description="Python driver for Arlyn scales.",
    package_dir={"":"arlyn"},
    packages=find_packages(where="arlyn"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/treychaffin/arlyn/",
    author="Trey Chaffin",
    author_email="tchaffin@aerosurvey.com",
    maintainer="Trey Chaffin",
    maintainer_email="tchaffin@aerosurvey.com",
    package_data={"arlyn": ["py.typed"]},
    install_requires=["pyserial"],
    license="GPLv2",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    ]
)