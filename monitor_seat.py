import asyncio
from kuksa_client.grpc.aio import VSSClient

async def main():
    async with VSSClient('127.0.0.1', 55555, root_certificates=None) as client:
        print("Connected to KUKSA Databroker.")
        print("Subscribing to Vehicle.Speed...")
        
        async for updates in client.subscribe_current_values(['Vehicle.Speed']):
            for path, value in updates.items():
                print(f"Update received: {path} = {value.value}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping monitor...")
