import sys
sys.path.append("..")
sys.path.append(".")
from PySqlTemplate import DBTypes, DataSource, PySqlTemplate

PySqlTemplate.set_data_source(
    DataSource(
        dbType=DBTypes.MySql,
        user='root',
        password='root',
        ip='127.0.0.1',
        port=3306,
        db='billing')
)

userModel = PySqlTemplate.findOne(
    'select * from user where username=? and passwd=?', 'admin', '123456')
print(userModel)
