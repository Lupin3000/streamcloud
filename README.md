# Streamcloud.eu download

Streamcloud.py is a simple and tiny Python script which helps to download movies from [streamcloud.eu](http://streamcloud.eu). Just copy URL and use as script argument. No need to search in HTML source code and to close millions of PopUps!

## Requirements

- Python (*2.7.x*)
- Python validators (*0.11.1*)
- Python requests (*2.12.1*)
- Python lxml (*3.6.4*)
- Python pycurl (*7.43.0*)

## Legal

No liability for any damage or functionality. *Script is tested with macOS Sierra (10.12.1)*! No liability for any illegal use!

## Usage

**Installation**

*Usage of [virtualenv](https://virtualenv.pypa.io/) is recommended and set proper file permission for Python script.*

```bash
# install packages via pip
$ sudo pip install -r requirements.txt
```

**Run script**

```bash
# show help
$ python -B streamcloud.py --help

# simple run
$ python -B streamcloud.py <url>

# run with defined output
$ python -B streamcloud.py <url> -o MyNewVideo.mp4
```

## FAQ

Q: Why that script?  
A: Because I got annoyed by the whole PopUps and search in source code.


Q: Is it legal?  
A: Depends to your local law and what you download.


Q: Parse video link does not work *(sometimes)*?  
A: Expand the waiting time on class constructor ```self.__seconds = 25``` *(default is 15 sec)*.


Q: Can i develop more on script by my own?  
A: Yes do it - You are welcome!!!


Q: Can I solve problems because of a proxy server!  
A: Yes, read on [PycURL](pycurl.io) documentation about ```pycurl.PROXY``` and so on.
