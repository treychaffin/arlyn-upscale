"""Install parameters for CLI and python import."""
from setuptools import setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name="arlyn",
    version="0.0.1",
    description="Python driver for Arlyn scales.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/treychaffin/arlyn/",
    author="Trey Chaffin",
    author_email="tchaffin@aerosurvey.com",
    maintainer="Trey Chaffin",
    maintainer_email="tchaffin@aerosurvey.com",
    packages=["arlyn"],
    package_data={"arlyn": ["py.typed"]},
    install_requires=["pyserial"],
    # extras_require={
    #         'test': [
    #             'pytest>=8,<9',
    #             'pytest-cov>=5,<6',
    #             'pytest-asyncio>=0.23.5',
    #             'pytest-xdist==3.*',
    #             'ruff==0.3.4',
    #             'mypy==1.9.0',
    #             'types-pyserial',
    #         ],
    #     },
    # entry_points={
    #     "console_scripts": [("alicat = alicat:command_line")]
    # },
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