import asyncio
import uvicorn

async def run_quart():
    config = uvicorn.Config("rk:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def other_tasks():
    print("Starting other async tasks...")
    await asyncio.sleep(2)
    print("Other async tasks completed!")

async def main():
    
    await asyncio.gather(
        run_quart(),
        other_tasks(),
    )


if __name__ == "__main__":
    asyncio.run(main())
