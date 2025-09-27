# src/passgan_stub.py
import random
import asyncio

async def passgan_stream(batch_size=100):
    # Replace this with real PassGAN sampler integration
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    for _ in range(batch_size):
        yield "".join(random.choice(chars) for _ in range(8))
