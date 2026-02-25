import asyncio
import logging
from kuksa_client.grpc.aio import VSSClient
from kuksa_client.grpc import Metadata

logging.basicConfig(level=logging.INFO)

async def main():
    async with VSSClient('127.0.0.1', 55555) as client:
        print("Connecting to Databroker...")
        
        # Register the seat position signal
        print("Registering Vehicle.Cabin.Seat.Row1.Pos1.Position")
        try:
            await client.set_metadata(
                updates={
                    'Vehicle.Cabin.Seat.Row1.Pos1.Position': Metadata(
                        data_type='uint8',
                        description='Seat position of row 1 pos 1',
                        entry_type='Actuator' # Or Sensor, Actuator allows set
                    )
                }
            )
            print("Registration successful!")
        except Exception as e:
            print(f"Registration failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
