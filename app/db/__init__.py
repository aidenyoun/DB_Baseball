from app.db.database import Base, engine

# 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
