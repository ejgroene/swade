import collections
import pandas
import selftest
import misc
test = selftest.get_tester(__name__)

""" Implements the functions 1..4 from "the slide" """

# 1.
def find_similarities(tables, ontology):
    similarities = collections.defaultdict(dict)
    for table in tables:
        for clazz in ontology.get_classes():
            similarities[table][clazz] = find_similarity(table, clazz)
    return similarities


# 2
def find_similarity(table, clazz):
    clazz_tablename_similarity = determine_match(table.name(), clazz.name())
    propertyname_columnname_similarities = collections.defaultdict(dict)
    for columnname in table.get_column_names():
        for propertyname in clazz.get_propertynames():
            propertyname_columnname_similarities[columnname][propertyname] = determine_match(columnname, propertyname)
    
    # 1. why do you pass clazz_tablename_similarity[i][j]? Did you mean to call compute_score outside of find_similarity?
    return compute_score(clazz_tablename_similarity, propertyname_columnname_similarities)


#2.a
def determine_match(a, b):
    if not a or not b:
        print(f"Warning: cannot match {a!r} with {b!r}.")
        return 0.0
    return float(len(set(a) & set(b)) / len(a))


@test
def matching_simple_terms():
    # something ridiculously simple as placholder
    test.eq(1.0, determine_match("ape", "ape"))
    test.eq(0.0, determine_match("ape", "boy"))
    test.eq(1/3, determine_match("ape", "pig"))


# 3
# why do you expect one similarity score in the second arguments? I'd expect all of them.
def compute_score(clazz_tablename_similarity, propertyname_columnname_similarities):
    return 1.0


@test
def main_function():
    tables = misc.read_tables(misc.testdatadir)
    test.eq(2, len(tables))
    ontology = misc.Ontology(misc.testdatadir)
    test.eq(108, len(ontology.get_classes()))
    similarities = find_similarities(tables, ontology)
    test.eq(len(tables), len(similarities))

