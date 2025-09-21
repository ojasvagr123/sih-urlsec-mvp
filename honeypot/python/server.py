#!/usr/bin/env python3
import asyncio
import datetime
import os
import signal
from handlers import handle_session
from logger import SessionLogger

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = int(os.environ.get("HONEYPOT_PORT", "2222"))
LOG_PATH = os.environ.get("HONEYPOT_LOG", "/cowrie/data/log/cowrie.session.log")

logger = SessionLogger(LOG_PATH)

async def client_connected(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info("peername")
    ip = peer[0] if peer else "unknown"
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    logger.info(f"{ts} - connect - src={ip}")
    try:
        await handle_session(reader, writer, ip, logger)
    except Exception as e:
        logger.info(f"{ts} - error - src={ip} - err={e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        logger.info(f"{ts} - disconnect - src={ip}")

async def main():
    server = await asyncio.start_server(client_connected, LISTEN_HOST, LISTEN_PORT)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[honeypot] Listening on {addrs}")
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set_result, None)
    await stop
    server.close()
    await server.wait_closed()

if __name__ == "__main__":
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[honeypot] stopped")
