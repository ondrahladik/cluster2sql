# cluster2sql

**cluster2sql** connects to a DX Cluster via telnet, parses incoming DX spots, and stores them in a relational database. It is designed for long-term archiving and analysis of DX activity.

#### Requirements

- Python 3.7+
- MySQL/MariaDB server  

## Configuration
Copy the `config.py.example` file to `config.py` and edit the variables to match your DX Cluster and database settings.

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