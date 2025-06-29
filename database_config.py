from database_local import LocalDatabaseManager

def get_database_manager():
    """
    Get local SQLite database manager for optimal performance.
    """
    print("Using local SQLite database for fast performance")
    return LocalDatabaseManager()

# For backward compatibility
def get_db():
    """Alias for get_database_manager"""
    return get_database_manager()