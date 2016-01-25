from app.config import ApplicationConfig

database_engine = ApplicationConfig.DATABASE_ENGINE

# Set stores based on config
if database_engine == 'mongo':
    from .mongo.mongo_resolution_store import MongoResolutionStore
    resolution_store = MongoResolutionStore()
else:
    raise RuntimeError("DATABASE_ENGINE not set or set to a value not implemented")
