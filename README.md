# cluster2sql

**cluster2sql** connects to a DX Cluster via telnet, parses incoming DX spots, and stores them in a relational database. It is designed for long-term archiving and analysis of DX activity.

#### Requirements

- Python 3.7+
- MySQL/MariaDB server  

## Configuration

Edit the following variables in the `cluster.py` file: 

```python
HOST = "cluster.example.com"      # DX Cluster address
PORT = 23                         # Port (usually 23 for telnet)
CALLSIGN = "YourCallsign"         # Your callsign

DB_CONFIG = {
    "host": "localhost",           # MySQL host
    "user": "root",                # MySQL user
    "password": "",                # MySQL password
    "database": "cluster"          # Database name
}
```