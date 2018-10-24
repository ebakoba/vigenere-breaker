# Vigenere cracker

## Description

  TODO

## Requirements

  1. [Python 3.7](https://www.python.org/downloads/)

  2. pipenv (just run ```pip install pipenv```)

## How to run

  1. ```pipenv install```
  
  2. ```pipenv run python ./main.py```

  3. open *localhost:8080* on latest Google Chrome

  4. Profit?

## Ideas

 * Cipher text will be broken when index of coincidence is [close to 0.0686](https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html)
 
 * To identify false positives during the real bruteforce method, we can use occurances of the word THE in the plain text

## Resources used

 * [English words](https://github.com/dwyl/english-words)
 * [Google 10000 most popular](https://github.com/first20hours/google-10000-english)
 * [Vigener decrypt algorithm in Python](https://inventwithpython.com/hacking/chapter19.html)
 * [Key length based on index of coincidence](https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC-Len.html)
 * [Inspiration for frequency score calculation](https://inventwithpython.com/hacking/chapter20.html)
 * [Help in parallel processing](https://stackoverflow.com/questions/30384568/how-to-get-the-first-finished-async-result-from-pool)
 * [Killing parallel processes](https://stackoverflow.com/questions/42782953/python-concurrent-futures-how-to-make-it-cancelable/45515052#45515052)