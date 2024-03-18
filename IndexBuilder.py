import validators
import rdflib
from rdflib import URIRef, Graph


class Property:
    count = 0

    def __init__(self):
        Property.count = Property.count + 1
        self.id = Property.count
        self.name: str = ''
        self.range: str = ''

    def print(self):
        print('Id: ', self.id)
        print('Name: ', self.name)
        print('Range: ', self.range)
        print('----------------')


class Concept:
    count = 0

    def __init__(self):
        Property.count = Property.count + 1
        self.id = Property.count
        self.name: str = ''
        self.parent: str = ''
        self.children = []
        self.attributes = []

    def print(self):
        print('Id: ', self.id)
        print('Name: ', self.name)
        print('Parent: ', self.parent)
        print('Attributes:')
        if len(self.attributes) > 0:
            for c in self.attributes:
                print('\t', c)
        else:
            print('<No Attributes>')
        print('Subclasses')
        if len(self.children) > 0:
            for c in self.children:
                print('\t', c)
        else:
            print('<No Subclasses>')

        print('----------------')


master_concepts = ['Pipe', 'WaterQuality']
concepts = list()
properties = list()


# def last_index(str, x):
#     index = -1
#     for i in range(0, len(str)):
#         if str[i] == x:
#             index = i
#     return index

def remove_prefix(n):
    if isinstance(n, rdflib.URIRef):
        s = n.split('#')[-1]
        if validators.url(s):
            return s.split('/')[-1]
        return s
    return n


def find_concept(name: str) -> Concept:
    for e in concepts:
        if e.name == name:
            return e

    return None


graph = Graph()
graph.parse(location="swade.ttl", format="ttl")
# graph.parse(location="saref4watr.ttl", format="ttl")
# graph.parse(location="saref4city.ttl", format="ttl")
# print(graph)

for sub, pred, obj in graph:
    sub = remove_prefix(sub)
    pred = remove_prefix(pred)
    obj = remove_prefix(obj)

    # print (sub, pred, obj)

    if pred == 'domain':
        c = find_concept(obj)
        if c == None:
            # create a concept and add to the concepts list
            c = Concept()
            c.name = obj
            concepts.append(c)
        c.attributes.append(sub)

    elif pred == 'subClassOf':
        if obj != type('str'):
            c = find_concept(obj)
            if c == None:
                # create a concept and add to the concepts list
                c = Concept()
                c.name = obj
                concepts.append(c)
            if not sub in c.children:
                c.children.append(sub)
            s = find_concept(sub)
            if s == None:
                # create a concept and add to the concepts list
                s = Concept()
                s.name = sub
                concepts.append(s)
            s.parent = obj

    elif pred == 'range':
        p = Property()
        p.name = sub
        p.range = obj
        properties.append(p)

for c in concepts:
    print(c.id, ',', c.name, ',', c.parent)

    # if sub == 'Pipe' or obj == 'Pipe':
    #     print(sub)
    #     print(pred)
    #     print(obj)

# -- Table: public.range_dataType
# -- DROP TABLE IF EXISTS public."range_dataType";


print(
    "CREATE TABLE IF NOT EXISTS range_datatype ( range text, datatype text, CONSTRAINT range_datatype_pkey PRIMARY KEY (range));")

# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public."range_dataType"
#     OWNER to postgres;


# -- Table: public.IsA_Relationships

# -- DROP TABLE IF EXISTS public."IsA_Relationships";

print(
    "CREATE TABLE IF NOT EXISTS isa_relationships (name text, parent text, CONSTRAINT isa_relationships_pkey PRIMARY KEY (name,parent));")

# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public."IsA_Relationships"
#     OWNER to postgres;

# -- Table: public.master_data_vocabs

# -- DROP TABLE IF EXISTS public.master_data_vocabs;

print(
    "CREATE TABLE IF NOT EXISTS master_data_vocabs (name text, CONSTRAINT master_data_vocabs_pkey PRIMARY KEY (name));")

# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.master_data_vocabs
#     OWNER to postgres;


for p in properties:
    print("INSERT INTO range_datatype VALUES ('", p.name, "', '", p.range, "');", sep="")

for c in concepts:
    if c.name in master_concepts:
        print("INSERT INTO master_data_vocabs VALUES ('", c.name, "');", sep="")

        # if c.parent != '':
        #     print ("INSERT INTO isa_relationships VALUES (", c.id,", '",c.name,"', '",find_concept(c.parent).name,"');",sep="")

    if len(c.children) > 0:
        for s in c.children:
            s_obj = find_concept(s)
            print("INSERT INTO isa_relationships VALUES ('", s_obj.name, "', '", c.name, "');", sep="")

            # CREATE TABLE COMPANY (
    # ID INT PRIMARY KEY     NOT NULL,
    # NAME           TEXT    NOT NULL,
    # AGE            INT     NOT NULL,
    # ADDRESS        CHAR(50),
    # SALARY         REAL
    # );
    col = ''
    if c.name in master_concepts:
        if len(c.attributes) > 0:
            for a in c.attributes:
                col = col + ',' + a + ' BOOLEAN '

        print('CREATE TABLE', c.name, '(org_name TEXT, city_name TEXT, Start INTEGER, ending_time INTEGER' + col + ');')
    print('-----------------')

#Insert some dummy data
print("INSERT INTO Pipe VALUES ('LAWD', 'Carson', 1960, 2020, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);")
print("INSERT INTO Pipe VALUES ('XYZ', 'Torrance', 1960, 2020, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE);")

