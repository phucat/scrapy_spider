On Ubuntu Machine, RUN the following commands:

#SCRAPER FOR YELLOW PAGE AND YELL
This scrapy uses scrapy library for python
https://scrapy.org/

install system libraries
```sh
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
(the virtual environment is also included on the source code in 'env' directory) just activate it.
$ . env/bin/activate
$ pip install scrapy
$ pip install retry
```

then run spider.
```sh
$ cd spiders
$ scrapy runspider yell.py -a search="Information Technology"
```

for the MSSQL connector to work, install the following

```sh
 sudo apt-get install unixodbc-dev
$ pip install pyodbc
$ pip install sqlalchemy
```
Follow this guide to download Drivers from Microsoft:
https://blogs.msdn.microsoft.com/sqlnativeclient/2016/10/20/odbc-driver-13-0-for-linux-released/

for http proxy install tor and polipo library
```sh
$ sudo apt install tor
$ sudo apt-get install polipo

Configure polipo  by following this guide:
http://pkmishra.github.io/blog/2013/03/18/how-to-run-scrapy-with-TOR-and-multiple-browser-agents-part-1-mac/
https://deshmukhsuraj.wordpress.com/2015/03/08/anonymous-web-scraping-using-python-and-tor/

Run tor and polipo
```sh
$ tor &
$ service polipo start
```