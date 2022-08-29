# Server Health Monitor

Install twisted:
```bash
pip3 install twisted
```

Install pycurl:
```bash
pip3 install pycurl
```

## run server
Execute "server.py" script:
```bash
./server.py
```

The server will run on localhost port 12345

You can use curl to view responses from the server:
curl http://127.0.0.1:12345

The server fails 25% of the time!!!