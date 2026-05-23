from .database import engine

try:
    connection = engine.connect()
    print("Connection connected successfully!")
    connection.close()
except Exception as e:
    print("Connection failed:")
    print(e)
