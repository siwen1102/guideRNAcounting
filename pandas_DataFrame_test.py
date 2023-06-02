import pandas as pd
import sqlalchemy

# convert Dataframe to excel
df = pd.DataFrame([['a','b'], ['c', 'd']], index = ['row1', 'row2'], columns = ['col1', 'col2'] )
#df.to_excel("output_test.xlsx")

# Constructing Dataframe from a dictionary
#df= pd.DataFrame({'col1': [1,2], 'col2': [3,4]})
engine = sqlalchemy.create_engine('sqlite:///test.db')
df.to_sql("test.db", engine, if_exists='append', index = False)