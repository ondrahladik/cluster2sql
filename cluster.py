import asyncio
import telnetlib3
import mysql.connector
import re
from config import DB_CONFIG, HOST, PORT, CALLSIGN

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

spot_regex = re.compile(
    r"DX de (\S+):\s+(\d+\.\d+)\s+(\S+)\s+(.*?)\s+(\d{4}Z)"
)

async def main():

    reader, writer = await telnetlib3.open_connection(
        HOST,
        PORT
    )

    print("Connected")

    while True:

        line = await reader.read(1024)

        if "login:" in line.lower():
            break

    writer.write(CALLSIGN + "\n")

    print("Logged in")

    while True:

        line = await reader.readline()

        if not line:
            continue

        line = line.strip()

        # print(line)

        # only DX spots
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

                cursor.execute(sql, values)
                db.commit()

                print(f"DX de {spotter}: {freq} MHz {dx}")
        
try:
    asyncio.run(main())

except KeyboardInterrupt:

    print("\nDisconnected")

    try:
        cursor.close()
        db.close()
    except:
        pass