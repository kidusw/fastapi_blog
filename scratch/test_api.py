import asyncio
import httpx

async def test_api():
    async with httpx.AsyncClient() as client:
        # Test main posts API
        response = await client.get("http://localhost:8001/api/posts?skip=0&limit=1")
        print("API Response (/api/posts):")
        print(response.status_code)
        print(response.json())
        
        # Test user posts API (assuming user 1 exists)
        response = await client.get("http://localhost:8001/api/users/1/posts?skip=0&limit=1")
        print("\nAPI Response (/api/users/1/posts):")
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    asyncio.run(test_api())
