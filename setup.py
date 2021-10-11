"""Setup script for mitype."""
from setuptools import setup

import versioneer

if __name__ == "__main__":
    setup(
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        download_url="https://github.com/mithil467/mitype/archive/v%s.tar.gz"
        % versioneer.get_version(),
    )
