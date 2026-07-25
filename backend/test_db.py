from app.database.database import Base
from app.database.models import Workspace, Document
from app.database.database import engine

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("Done")