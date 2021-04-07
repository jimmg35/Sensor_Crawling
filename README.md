# Sensor_Crawling

This is my little project! :)

## Dependency
```
pip install requests==2.22.0
pip install schedule==0.6.0
pip install psycopg2==2.7.7
PostgreSQL 12.2, compiled by Visual C++ build 1914, 64-bit
```

## Usage
```python
# initialize basic object.
myKey = Key()
myBundler = UrlBundler()
myReq = Requester(myBundler, myKey)

# initialize dbcontext
myDBcontext = Dbcontext({"user":"postgres",
                            "password":"jim60308",
                            "host":"localhost",
                            "port":"5432"}, "sensordata")
myStorage = Storer(myDBcontext)
```