
"""
##connection information
##class initialization
##db insert
"""
from sqlalchemy import create_engine, Table, Column, MetaData, select
import pyodbc
from BotHelperFunctions import Listize_DB_Result
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('appconfig.cfg')
connectstring = config.get('DBConfig','engine_string')
tablestring = config.get('DBConfig', 'table_string')

class DataAccessor:
    """class to access db"""

    def __init__(self):
        self.db = create_engine(connectstring)
        self.meta = MetaData()
        self.meta.reflect(self.db)
        self.conn = self.db.connect()
        self.submission_table = self.meta.tables[tablestring]
        
    def Insert_Submissions(self, insert_set):
        ins = self.submission_table.insert()
        self.conn.execute(ins, insert_set)

    def Get_Previous_Submission_IDs(self):
        sel = select([self.submission_table.c.SubmissionID]).order_by(self.submission_table.c.PostDate.desc())
        result = Listize_DB_Result(self.conn.execute(sel).fetchall())
        return result