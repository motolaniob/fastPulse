# Test raw asgi application for debugging and testing FastPulse
async def application(scope, receive, send):
    print(scope)
    async def logged_receive():
        receive_copy = await receive()
        print(receive_copy)
        return receive_copy
    async def logged_send(message):
        print(message)
        await send(message)
    if scope["type"] == "http":
        await logged_receive()
        await logged_send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain")]})
        await logged_send({"type": "http.response.body", "body": b"hello"})
        await logged_receive()

    elif scope["type"] == "lifespan":
        while True:
            message = await logged_receive()
            if message["type"] == "lifespan.startup":
                await logged_send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await logged_send({"type": "lifespan.shutdown.complete"})
                return

