from distutils.core import setup
setup(
    name='mitype',
    packages=['mitype'],
    version='0.1.2',
    license='GPL',
    description='A command line tool to improve typing speed',
    author='MITHIL POOJARY',
    author_email='mithil467@gmail.com',
    url='https://github.com/mithil467/mitype',
    download_url='https://github.com/mithil467/mitype/archive/v0.1.2.tar.gz',
    keywords=['TYPE', 'MITYPE', 'WPM'],
    install_requires=[
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_data={"mitype": ["data.db"]},
    include_package_data=True,
    zip_safe=False
)

