import asyncio
from arq.connections import RedisSettings
import random
from arq import Retry

async def generate_weekly_report(ctx , user_email: str):

    attempt = ctx['job_try']

    print(f"📥 Generating weekly report for {user_email}...")
    await asyncio.sleep(2)
    
    # Simulate a 70% chance that the email server crashes
    if random.random() < 0.7:
        print("❌ CRASH: The email server is down!")
        if attempt < 3:
            delay = attempt * 5 # Wait 5s, then 10s
            print(f"⏳ Waiting {delay} seconds before trying again...")
            raise Retry(defer=delay) 
        else:
            print("💀 DEAD-LETTER: Failed 3 times. Giving up and alerting engineering.")
            raise Exception("Permanent failure.")


        
    print(f"✅ Generated weekly report for {user_email}...")
    return True


class WorkerSettings:
    functions = [generate_weekly_report]
    redis_settings = RedisSettings(host="localhost", port=6379)