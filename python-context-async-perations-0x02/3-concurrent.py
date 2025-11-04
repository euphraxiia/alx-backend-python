import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        List of all users from the database
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        return results

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        List of users older than 40
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        return results

async def fetch_concurrently():
    """
    Execute both queries concurrently using asyncio.gather.
    
    Returns:
        Tuple containing results from both queries
    """
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Use asyncio.run() to run the concurrent fetch
if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Users older than 40:", older_users)

