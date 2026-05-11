import asyncio
import telnetlib3
import mysql.connector
import re
import sys
from datetime import datetime
from config import DB_CONFIG, HOST, PORT, CALLSIGN

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

spot_regex = re.compile(
    r"DX de (\S+):\s+(\d+\.\d+)\s+(\S+)\s+(.*?)\s+(\d{4}Z)"
)

async def reconnect_loop():
    while True:
        try:
            await main()
        except Exception as e:
            print(f"[{datetime.now()}] Connection error: {e}", file=sys.stderr)
            print(f"[{datetime.now()}] Reconnecting in 5 seconds...", file=sys.stderr)
            await asyncio.sleep(5)

async def main():
    try:
        reader, writer = await asyncio.wait_for(
            telnetlib3.open_connection(HOST, PORT),
            timeout=10
        )
    except asyncio.TimeoutError:
        raise Exception("Connection timeout")

    print(f"[{datetime.now()}] Connected to {HOST}:{PORT}")

    login_timeout = 30
    login_found = False
    start_time = asyncio.get_event_loop().time()

    while True:
        try:
            line = await asyncio.wait_for(reader.read(1024), timeout=login_timeout)
            
            if "login:" in line.lower():
                login_found = True
                break
                
            if asyncio.get_event_loop().time() - start_time > login_timeout:
                raise Exception("Login prompt not found within timeout")
        except asyncio.TimeoutError:
            if not login_found:
                raise Exception("No data received during login phase")

    writer.write(CALLSIGN + "\n")
    print(f"[{datetime.now()}] Logged in as {CALLSIGN}")

    while True:
        try:
            line = await asyncio.wait_for(reader.readline(), timeout=120)

            if not line:
                await asyncio.sleep(0.1)
                continue

            line = line.strip()

            if line.startswith("DX de"):
                match = spot_regex.search(line)

                if match:
                    spotter = match.group(1)
                    freq = float(match.group(2))
                    dx = match.group(3)
                    message = match.group(4).strip()

                    sql = """
                        INSERT INTO cluster
                        (
                            spotter,
                            freq,
                            dx,
                            message
                        )
                        VALUES (%s, %s, %s, %s)
                    """

                    values = (
                        spotter,
                        freq,
                        dx,
                        message
                    )

                    try:
                        cursor.execute(sql, values)
                        db.commit()
                        print(f"[{datetime.now()}] DX de {spotter}: {freq} MHz {dx}")
                    except mysql.connector.Error as e:
                        db.rollback()
                        print(f"[{datetime.now()}] DB error: {e}", file=sys.stderr)
                        
        except asyncio.TimeoutError:
            print(f"[{datetime.now()}] No data received for 120s, reconnecting...", file=sys.stderr)
            raise Exception("Read timeout")
        
try:
    asyncio.run(reconnect_loop())

except KeyboardInterrupt:
    print(f"\n[{datetime.now()}] Disconnected by user")
    try:
        cursor.close()
        db.close()
    except:
        pass