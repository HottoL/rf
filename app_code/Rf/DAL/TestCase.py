import __init__
from System.Db.orm import Model, StringField, IntegerField

class TestCase(Model):
    __table__ = "testcase"
    caseId = IntegerField(primary_key=True)
    caseName = StringField()


'''
CREATE TABLE testcase 
(
    caseId int NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY(caseID),
    caseName varchar(100)
)
'''