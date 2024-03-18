import validators
import rdflib
from rdflib import Graph, Namespace, exceptions
from rdflib import URIRef, RDFS, RDF, BNode
from rdflib.namespace import OWL


def remove_prefix(n):
    if isinstance(n, rdflib.URIRef):
        s = n.split('#')[-1]
        if validators.url(s):
            return s.split('/')[-1]
        return s
    return n


def find_and_remove_class(name, classes):
    for c in classes:
        if c["name"] == name:
            classes.remove(c)
            return c


def find_root_classes(classes):
    root_classes = []
    for c in classes:
        if len(c["parents"]) == 0:
            root_classes.append(c)

    for c in root_classes:
        classes.remove(c)

    return root_classes


def print_tree(root, classes):
    if root == None:
        return

    print(root)

    if root["subClasses"] != []:
        for c in root["subClasses"]:
            n = find_and_remove_class(c, classes)
            print_tree(n, classes)


graph = Graph()
graph.parse(location="swade.ttl", format="turtle")
graph.parse(location="saref4city.ttl", format="turtle")
graph.parse(location="saref4watr.ttl", format="turtle")

classes = list()
for s1, p1, o1 in graph.triples((None, RDF.type, OWL.Class)):
    new_class = {"name": remove_prefix(s1)}

    # #comment
    for c in graph.objects(subject=s1, predicate=RDFS.comment):
        new_class["comment"] = c.toPython()
        break

    # label
    for l in graph.objects(subject=s1, predicate=RDFS.label):
        new_class["label"] = l.toPython()
        break

    # subclass of
    parents = []
    for p in graph.objects(subject=s1, predicate=RDFS.subClassOf):
        if type(p) != rdflib.BNode:
            parents.append(remove_prefix(p))
    new_class["parents"] = parents

    # sub classes
    sub_classes = []
    for sc in graph.subjects(predicate=RDFS.subClassOf, object=s1):
        sub_classes.append(remove_prefix(sc))
    new_class["subClasses"] = sub_classes

    # individuals
    individuals = []
    for i in graph.subjects(predicate=RDF.type, object=s1):
        individuals.append(remove_prefix(i))
    new_class["individuals"] = individuals

    # properties
    object_properties = []
    data_properties = []
    for p in graph.subjects(predicate=RDFS.domain, object=s1):

        # get the range of this property
        r = graph.value(subject=p, predicate=RDFS.range)
        # check the type of this property
        pt = graph.value(subject=p, predicate=RDF.type)
        if pt == OWL.DatatypeProperty:
            data_properties.append({"name": remove_prefix(p), "type": remove_prefix(r)})
        elif pt == OWL.ObjectProperty:
            object_properties.append({"name": remove_prefix(p), "type": remove_prefix(r)})
    new_class["dataProperties"] = data_properties
    new_class["objectProperties"] = object_properties

    classes.append(new_class)

# for c in classes:
#     if len(c["parents"]) == 0:
#         print(c)
root_classes = find_root_classes(classes)
for r in root_classes:
    print_tree(r, classes)

