**********
⌨ Mitype ⌨
**********

|Climate| |PyPI Latest Release| |License| |Black|

.. |PyPI Latest Release| image:: https://img.shields.io/pypi/v/mitype.svg
    :target: https://pypi.org/project/mitype/

.. |License| image:: https://img.shields.io/pypi/l/mitype.svg
    :target: LICENSE.txt

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. |Climate| image:: https://api.codeclimate.com/v1/badges/4d0397d4c7dd3b81a205/maintainability
   :target: https://codeclimate.com/github/Mithil467/mitype/maintainability
   :alt: Maintainability


|Demo|

.. |Demo| image:: img/screen.gif
    :target: img/screen.gif

What is it?
===========

**Mitype** is a Python package to test (and hence improve) your typing speed right from the ease of your terminal. 

Features
========

- For Linux, Windows and macOS  
- Runs on python 3 and 2 both
- No external dependencies*   
- Choose custom text from a file  
- And difficulty level  
-  Or let the app decide! (From over 6000️ text sets)  
- Colored texts  


* For windows, you need windows-curses to run

Where to get it?
================

The source code is hosted on GitHub at:
https://github.com/mithil467/mitype

.. _Python package index: https://pypi.org/project/mitype/#files

``pip install mitype``

That's all if you are on linux and mac OS.
If you are on windows, you also need windows-curses, which can be installed from pypi:

``pip install windows-curses``

How to run it?
==============

Once installed, you can run it by

``python -m mitype``

You can choose difficulty in between 1 and 5.

```python -m mitype -d <value>``

Example:

```python -m mitype -d 2``

You can use text from your own file by

``python -m mitype -f SampleTextFile``


You can quit the app anytime by pressing the **ESC** key.

Do directly run from repo:

```python local_host.py```

Dependencies
============

For windows only - `windows-curses`_.

.. _windows-curses: https://pypi.org/project/windows-curses

Installation from sources
=========================

To install ``mitype`` from source - 

In the ``mitype`` directory (same one where you found this file after
cloning the git repo), execute:

``python setup.py install``

License
=======

`GPL`_

.. _GPL: license.txt

Test text is taken from data.db database which is a collection of 6000 strings taken from typeracerdata.com (not given under my license).
