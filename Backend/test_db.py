from app.db.database import AsyncSessionLocal 
from app.models.daily_entry import DailyEntry
from app.utils.time import now_ist
db = AsyncSessionLocal()

try:
    # 1. Fetch just the date from the very first DailyEntry
    entry_row = db.query(DailyEntry.date).first()
    
    if entry_row:
        # entry_row is a Tuple, so we get the first item [0]
        date_value = entry_row[0] 
        print(now_ist().date() <= date_value)
        print(f"The value is: {date_value}")
        print(f"The exact Python type is: {type(date_value)}")
    else:
        print("No daily entries found in the database!")

finally:
    pass
