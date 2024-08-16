import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8c4EF9vXi8TZe6581e0af85c25'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'admin'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'IntelliMetr!c$'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'DbIntelliMetrics'

