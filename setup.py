""" Setup script for mitype """

from setuptools import setup

with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="mitype",
    packages=["mitype"],
    version="0.1.3",
    license="GPL",
    description="A command line tool to improve typing speed",
    author="MITHIL POOJARY",
    author_email="mithil467@gmail.com",
    url="https://github.com/mithil467/mitype",
    download_url="https://github.com/mithil467/mitype/archive/v0.1.3.tar.gz",
    keywords=["TYPE", "MITYPE", "WPM"],
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_data={"mitype": ["data.db"]},
    include_package_data=True,
    zip_safe=False,
)
