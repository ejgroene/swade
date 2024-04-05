import rdflib
import selftest

test = selftest.get_tester(__name__)

@test
def assumption_about_matching():
    g = rdflib.Graph()
    t = (rdflib.URIRef("http://an.uir/42"), rdflib.RDF.type, rdflib.Literal("my assumption"))
    g.add(t)
    # for ways to use a generator
    test.eq(t, next(g.triples((None, None, None))))
    test.eq(t, g.triples((None, None, None)).send(None))
    test.eq([t], list(g.triples((None, None, None))))
    for t2 in g.triples((None, None, None)):
        test.eq(t, t2)
    result = g.triples((
        None, rdflib.RDF.type, rdflib.Literal("my assumption")
    ))
    test.eq([t], list(result))
    result = g.triples((
        None, rdflib.RDF.type, rdflib.Literal("my assumption", lang='en')
    ))
    test.eq([], list(result))

@test
def assumption_about_matching_other_way_around():
    g = rdflib.Graph()
    t = (rdflib.URIRef("http://an.uir/42"), rdflib.RDF.type, rdflib.Literal("my assumption", lang='en'))
    g.add(t)
    test.eq([t], list(g.triples((None, None, None))))
    result = g.triples((
        None, rdflib.RDF.type, rdflib.Literal("my assumption")
    ))
    test.eq([], list(result))
    result = g.triples((
        None, rdflib.RDF.type, rdflib.Literal("my assumption", lang='en')
    ))
    test.eq([t], list(result))
