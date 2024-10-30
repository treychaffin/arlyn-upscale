"""Install parameters for CLI and python import."""
from setuptools import setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name="arlynupscale",
    version="0.0.6",
    description="Python driver for Arlyn UpScale Indicators.",
    packages=["arlynupscale"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/treychaffin/arlyn-upscale/",
    author="Trey Chaffin",
    author_email="treychaffin@gmail.com",
    maintainer="Trey Chaffin",
    maintainer_email="treychaffin@gmail.com",
    package_data={"arlyn-upscale": ["py.typed"]},
    install_requires=["pyserial"],
    extras_require={
        'test': [
            'pytest>=8,<9',
            'pytest-asyncio>=0.23.5',
        ],
    },
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
    ],
)