#!/usr/bin/env python3
import asyncio
import datetime

PROMPT = "ubuntu@server:~$ "
COMMAND_KB = {
    "uname -a": "Linux ubuntu 5.4.0-100-generic #1 SMP Tue Jan 1 00:00:00 UTC 2025 x86_64 GNU/Linux\n",
    "whoami": "root\n",
    "id": "uid=0(root) gid=0(root) groups=0(root)\n",
    "ls": "bin  boot  dev  etc  home  tmp  usr  var\n",
    "pwd": "/root\n",
    "exit": None,
}

async def send(writer, text):
    writer.write(text.encode())
    await writer.drain()

async def prompt(writer):
    await send(writer, PROMPT)

async def read_line(reader):
    data = await reader.readline()
    if not data:
        return None
    return data.decode(errors="ignore").rstrip("\r\n")

async def handle_session(reader, writer, src_ip, logger):
    await send(writer, "SSH-2.0-OpenSSH_7.9p1 Ubuntu-10\r\n")
    await send(writer, "Welcome\r\n")
    await prompt(writer)

    while True:
        line = await read_line(reader)
        if line is None:
            break
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        logger.info(f"{ts} - session - src={src_ip} - cmd={line}")
        cmd = line.strip()
        if cmd == "":
            await prompt(writer)
            continue
        if cmd in COMMAND_KB:
            resp = COMMAND_KB[cmd]
            if resp is None:
                await send(writer, "logout\n")
                break
            await send(writer, resp)
            await prompt(writer)
            continue
        # naive handling for common downloader attempts
        if any(tok in cmd for tok in ["wget ", "curl ", "nc ", "bash -i", "sh -i", "python -c"]):
            await send(writer, "bash: command not found\n")
            await prompt(writer)
            continue
        await send(writer, f"-bash: {cmd}: command not found\n")
        await prompt(writer)
