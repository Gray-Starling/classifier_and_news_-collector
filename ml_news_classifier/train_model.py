from src.preprocess import preprocess_data
from src.train import train
import asyncio

from data.get_data import download_data

async def main():
    file_path = "data/source/news_dataset.csv"
    await download_data(file_path)
    preprocess_data(file_path)
    train()

if __name__ == "__main__":
    asyncio.run(main())