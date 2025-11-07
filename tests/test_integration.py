from app.models import engine

def test_database_connection():
  try:
    connection = engine.connect()
    assert not connection.closed
  finally:
    connection.close()
