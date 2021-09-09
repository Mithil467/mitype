<h1 align="center"> ⌨ Mitype ⌨ </h1>
<p align="center">
    Typing Speed Test in Terminal 
    <br />
  <br />
<a href="https://codeclimate.com/github/Mithil467/mitype/maintainability"><img src="https://api.codeclimate.com/v1/badges/4d0397d4c7dd3b81a205/maintainability"></a>
<a href="https://pypi.org/project/mitype/"><img src="https://img.shields.io/pypi/v/mitype.svg"></a>
<a href="LICENSE.txt"><img src="https://img.shields.io/pypi/l/mitype.svg"></a>
<a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<br />
<img src="docs/source/_static/demo.gif" alt=>
</p>

**Mitype** is a program to test (and hence improve) your typing speed right from the ease of your terminal.

Written completely in python with no external dependencies!

## ✨ Main Features

- 🖥️ Cross-platform
- 🎦 See your replay
- 📝 Choose custom text input
- 🅰️ 6000 text samples
- 🌈 Colored texts

## 🔧 Install

Mitype can be easily installed by:

```pip install mitype```

## 📈 Usage

Once installed, you can run it simply as:

```mitype```

You can also customize each run by specifying the following options as:

- ```-f FILENAME, --file FILENAME```  
  Uses contents of file as sample text.  
- ```-d N, --difficulty N```  
  N can be in range [1, 5] with 1 being the easiest. This decides the length of the text.  
- ```-i ID, --id ID```  
  ID can be in range [1, 6000].  

You can quit mitype anytime by pressing the `ESC` key or `CTRL-C`.

You can also directly [run on repl.it](https://mitype.mithil467.repl.run/) in your web browser although, the latency is pretty high.

## 💚 Contributing

We encourage you to contribute to mitype! Please check out the [Contributing Guidelines](CONTRIBUTING.md) about how to proceed.

## 📜 License

Licensed under the [GPL](LICENSE.txt) license.

Text samples in database are collected from [Typeracer Data](http://typeracerdata.com/texts).
