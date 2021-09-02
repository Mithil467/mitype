"""Setup script for mitype."""
import io

from setuptools import setup

import versioneer

with io.open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="mitype",
    packages=["mitype"],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="GPL",
    description="A command line tool to improve typing speed",
    author="MITHIL POOJARY",
    author_email="mithil467@gmail.com",
    url="https://github.com/mithil467/mitype",
    download_url="https://github.com/mithil467/mitype/archive/v0.2.2.tar.gz",
    keywords=["MITYPE", "TERMINAL", "WPM", "SPEED", "TYPE"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=["windows-curses; platform_system=='Windows'"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    entry_points={
        "console_scripts": ["mitype=mitype.app:App"],
    },
)
