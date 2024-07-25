from src.preprocess import preprocess_data
import asyncio

async def main():
    await preprocess_data()
    # Добавьте другие шаги обработки данных здесь, если необходимо

if __name__ == "__main__":
    asyncio.run(main())