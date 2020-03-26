<h1 align="center"> ⌨ Mitype ⌨ </h1>
<p align="center">
    Typing Speed Test in your Terminal 
    <br />
  <br />
<a href="https://codeclimate.com/github/Mithil467/mitype/maintainability"><img src="https://api.codeclimate.com/v1/badges/4d0397d4c7dd3b81a205/maintainability"></a>
<a href="https://pypi.org/project/mitype/"><img src="https://img.shields.io/pypi/v/mitype.svg"></a>
<a href="LICENSE.txt"><img src="https://img.shields.io/pypi/l/mitype.svg"></a>
<a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<br />
<img src="img/demo.gif">
</p>

### What is it?

**Mitype** is a Python package to test (and hence improve) your typing speed right from the ease of your terminal.
Features

🖥️ For Linux, Windows and macOS  

🎦 See your replay!

🐍 Runs on python 3 and 2 both  

😊 No external dependencies*  

📝 Choose custom text from a file  

🤸 And difficulty level

😉 Or let the app decide! (From over 6000️ text sets)  

🌈 Colored texts

* For windows, you need windows-curses to run  

### Where to get it?

The source code is hosted on GitHub at: [mithil467/mitype](https://github.com/Mithil467/mitype)

```pip install mitype```

That's all if you are on linux and mac OS. If you are on windows, you also need windows-curses, which can be installed from pypi:

```pip install windows-curses```

### How to run it?

Once installed, you can run it by

```python -m mitype```

You can choose difficulty in between 1 and 5.

```python -m mitype -d <value>```

Example:

```python -m mitype -d 2```

You can use text from your own file by

```python -m mitype -f SampleTextFile```

You can quit the app anytime by pressing the *ESC* key.

To directly run from clone:

```python local_host.py```

### Dependencies

For windows only - [windows-curses](https://pypi.org/project/windows-curses/).

### Installation from sources

To install mitype from source -

In the mitype directory (same one where you found this file after cloning the git repo), execute:

```python setup.py install```

### License

[GPL](LICENSE.txt)

Test text is taken from data.db database which is a collection of 6000 strings taken from typeracerdata.com (not given under my license).
