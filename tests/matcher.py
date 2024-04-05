import pathlib
import selftest
test = selftest.get_tester(__name__)
import pandas as pd



def read_columns_names(file_path):
    df = pd.read_csv(file_path)
    return [s.strip() for s in df.columns.tolist()]


@test
def get_table_name(tmp_path):
    some_file = tmp_path/'myfile.cvs'
    some_file.write_text("A, B, C\n 1, 2, 3\n")
    columns = read_columns_names(some_file.as_posix())
    test.eq(['A', 'B', 'C'], columns)

@test
def get_match():
    trible = {[s,p,o],}
    tables_names ={['table1']}
    column_names={table:[col1,colm1,], table:[col]}
    match_table_className={[table:classn], ...}
    result = match_table_className({data})
    test.eq('classA', result)