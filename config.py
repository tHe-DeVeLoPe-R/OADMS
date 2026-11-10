"""
Urwat il Wusqa Travels (UTW) - DMS Configuration
Configured for TiDB Cloud Serverless (MySQL) with graceful local fallback.
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'utw-secret-key-zafar-786')
    
    # TiDB Cloud Serverless (MySQL) Settings
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 4000))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'BmvZHAeUxs9Xtca.root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'r6jxIc04MFIKJLRa')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'utw_dms')
    
    # Auto-detect or force SSL for remote cloud databases
    MYSQL_SSL = os.environ.get('MYSQL_SSL', 'true').lower() in ('true', '1', 'yes')
    
    # Path to CA Certificate (isrgrootx1.pem for TiDB Cloud)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MYSQL_SSL_CA = os.environ.get('MYSQL_SSL_CA', os.path.join(BASE_DIR, 'isrgrootx1.pem'))

    # Connection URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
