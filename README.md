RUN the following commands:

```sh
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
pip install scrapy
pip install retry

cd spiders
scrapy runspider yell.py -a search="Information Technology"
```


for the MSSQL connector to work, install the following

```sh
 sudo apt-get install unixodbc-dev
$ pip install pyodbc
$ pip install sqlalchemy
$ https://blogs.msdn.microsoft.com/sqlnativeclient/2016/10/20/odbc-driver-13-0-for-linux-released/
```

for http proxy
```sh
$ sudo apt install tor
$ sudo apt-get install polipo
```
http://pkmishra.github.io/blog/2013/03/18/how-to-run-scrapy-with-TOR-and-multiple-browser-agents-part-1-mac/
https://deshmukhsuraj.wordpress.com/2015/03/08/anonymous-web-scraping-using-python-and-tor/

