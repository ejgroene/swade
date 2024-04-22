import collections
import pandas
import statistics
import selftest
import misc
test = selftest.get_tester(__name__)


""" Implements the functions 1..4 from "the slide" """

class Algorithm:
    def __init__(self, tables, ontology):
        self.tables = tables
        self.ontology = ontology

    # 1.
    def find_similarities(self):
        similarities = collections.defaultdict(dict)
        for table in self.tables:
            for clazz in self.ontology.get_classes():
                similarities[table.name()][clazz.name()] = self.find_similarity(table, clazz)
        return similarities


    # 2
    def find_similarity(self, table, clazz):
        clazz_tablename_similarity = self.determine_match(table.name(), clazz.name())
        propertyname_columnname_similarities = collections.defaultdict(dict)
        for columnname in table.get_column_names():
            for propertyname in clazz.get_propertynames():
                propertyname_columnname_similarities[columnname][propertyname] = self.determine_match(columnname, propertyname)    
        try:
            return self.compute_score(clazz_tablename_similarity, propertyname_columnname_similarities)
        except AssertionError as e:
            print(f"WARNING: Cannot compute score for {table.name()} and {clazz.name()}. Reason: {e}")

    #2.a
    def determine_match(self, a, b):
        if not a or not b:
            print(f"Warning: cannot match {a!r} with {b!r}.")
            return 0.0
        return float(len(set(a) & set(b)) / len(a))


    # 3
    def compute_score(self, clazz_tablename_similarity, propertyname_columnname_similarities):
        assert len(propertyname_columnname_similarities) > 0, f"No property similarities."
        m = 1
        n = 0
        for columnname, properties in propertyname_columnname_similarities.items():
            for propertyname, match in properties.items():
                m = m + match
                n += 1
        return 0.4 * clazz_tablename_similarity + 0.6 * m / n


class AlgTest(Algorithm):
    pass


@test
def matching_simple_terms():
    ta = AlgTest(None, None)
    # something ridiculously simple as placholder
    test.eq(1.0, ta.determine_match("ape", "ape"))
    test.eq(0.0, ta.determine_match("ape", "boy"))
    test.eq(1/3, ta.determine_match("ape", "pig"))
    test.eq(0.5, ta.determine_match("material", "has duration"))



@test
def main_function_find_all_similarities_between_table_and_class():
    tables = misc.read_tables(misc.testdatadir)
    test.eq(2, len(tables))
    ontology = misc.Ontology(misc.testdatadir)
    test.eq(127, len(ontology.get_classes()))
    ta = AlgTest(tables, ontology)
    similarities = ta.find_similarities()
    test.eq(len(tables), len(similarities))
    test.truth("Pipe_city_b" in similarities)
    test.truth("city_A_pip" in similarities)
    pipe_sim = similarities["city_A_pip"]["Pipe"]
    test.eq(1.0, pipe_sim)