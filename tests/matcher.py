import pathlib
import selftest
test = selftest.get_tester(__name__)
import pandas as pd
import os

directory_path = r'C:\Users\gg363d\Source\Repos\swade\data'



def get_csv_table_names(directory_path):
    try:
        table_names = []
        # List all files and directories in the specified directory
        for filename in os.listdir(directory_path):
            # Check if the file ends with '.csv'
            if filename.endswith('.csv'):
                # Remove the '.csv' extension and append the file name to the list
                table_name = filename[:-4]
                table_names.append(table_name)
        return table_names
    except Exception as e:
        print("An error occurred:", e)
        

def get_columns_names(file_path):
    df = pd.read_csv(file_path)
    return [s.strip() for s in df.columns.tolist()]



@test
def test_get_columns_names(tmp_path):
    some_file = tmp_path/'myfile.cvs'
    some_file.write_text("a, b, c\n 1, 2, 3\n")
    columns = get_columns_names(some_file.as_posix())
    test.eq(['a', 'b', 'c'], columns)


@test
def test_get_table_names(tmp_path):
    some_file = tmp_path/'myfile.cvs'
    some_file.write_text("a, b, c\n 1, 2, 3\n")
    tables = test_get_table_names(some_file.as_posix())
    
table_names = get_csv_table_names(directory_path)
print (table_names)
column_names = get_columns_names(directory_path)
print (column_names)

# @test
# def get_match():
#     trible = {[s,p,o],}
#     tables_names ={['table1']}
#     column_names={table:[col1,colm1,], table:[col]}
#     match_table_className={[table:classn], ...}
#     result = match_table_className({data})
#     test.eq('classA', result)