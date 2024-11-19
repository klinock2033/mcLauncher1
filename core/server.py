import asyncio

async def server_status(ip: str, port: int):
    """ verificam status server """
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.close()
        await writer.wait_closed()
        return True, None
    except Exception as e:
        return False, str(e)