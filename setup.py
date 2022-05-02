from setuptools import find_packages, setup

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mease_elabftw",
    version="0.0.6",
    author="Liam Keegan",
    author_email="liam@keegan.ch",
    description="Extracts metadata from eLabFTW experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssciwr/mease-elabftw",
    project_urls={
        "Documentation": "https://mease-elabftw.readthedocs.io/",
        "Issues": "https://github.com/ssciwr/mease-elabftw/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="MIT",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "elabftw-list = mease_elabftw.scripts.cli:elabftw_list",
        ]
    },
    zip_safe=False,
)
