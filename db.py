from sqlalchemy import create_engine

__engine = None


def get_engine():
    global __engine
    if not __engine:
        __engine = create_engine(
            "mysql+pymysql://stock:stockPolarDBX@tencloud.co2penguin.top:15781/stockdb",
            echo=True,
            pool_recycle=3600,
        )
    return __engine


__all__ = ["get_engine"]
