import asyncio
import aiosqlite

# --- Step 1: Create example database (for demonstration) ---
async def setup_database():
    async with aiosqlite.connect("example.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.execute("DELETE FROM users")  # clear previous data
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Alice", 25),
                ("Bob", 45),
                ("Charlie", 32),
                ("Diana", 50),
                ("Eve", 41),
            ],
        )
        await db.commit()


# --- Step 2: Define async functions to fetch users ---
async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users


async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users


# --- Step 3: Run both queries concurrently ---
async def fetch_concurrently():
    # Run both at the same time using asyncio.gather
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )

    print("All Users:")
    for u in users:
        print(u)

    print("\nUsers older than 40:")
    for u in older_users:
        print(u)


# --- Step 4: Run the async function ---
if __name__ == "__main__":
    asyncio.run(setup_database())
    asyncio.run(fetch_concurrently())
