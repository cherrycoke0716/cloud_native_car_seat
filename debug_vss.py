import asyncio
import logging
from kuksa_client.grpc.aio import VSSClient
from kuksa_client.grpc import Metadata

logging.basicConfig(level=logging.INFO)

async def main():
    print("Initializing VSSClient...")
    print("Initializing VSSClient...")
    try:
        # Explicitly disable TLS verification by passing root_certificates=None
        async with VSSClient('127.0.0.1', 55555, root_certificates=None) as client:
            print("Connected to Databroker!")
            
            # Check if set_metadata exists
            if hasattr(client, 'set_metadata'):
                print("Method set_metadata exists.")
            else:
                print("Method set_metadata DOES NOT exist.")
                print(f"Available methods: {dir(client)}")
                return # Exit if not available

            # Register the seat position signal
            print("Registering Vehicle.Cabin.Seat.Row1.Pos1.Position")
            try:
                await client.set_metadata(
                    updates={
                        'Vehicle.Cabin.Seat.Row1.Pos1.Position': Metadata(
                            data_type='uint8',
                            description='Seat position of row 1 pos 1',
                            entry_type='Actuator' 
                        )
                    }
                )
                print("Registration successful!")
            except Exception as e:
                print(f"Registration failed: {e}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
