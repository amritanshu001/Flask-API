from sqlalchemy import create_engine
from dbconnection.config import config
import platform


def get_engine():
    if platform.system() == 'Linux':
        database = config(filename='linux_connect.ini')
    else:
        database = config(filename='connect.ini')

    dialect = 'postgresql'
    driver = 'psycopg2'
    port = '5432'
    user = database['user']
    passwd = database['password']
    host = database['host']
    db = database['database']

    url = f"{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{db}"
    # if not database_exists(url):
    #    create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return [url, engine]
