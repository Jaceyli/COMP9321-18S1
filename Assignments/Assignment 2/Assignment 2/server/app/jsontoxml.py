import dicttoxml
from xml.dom.minidom import parseString

from feedgen.feed import FeedGenerator


def toxml(json):
    xml = dicttoxml.dicttoxml(json)
    dom = parseString(xml)
    return dom.toprettyxml()


def tofeed(results, detail=True):
    fg = FeedGenerator()
    fg.title('Results')
    fg.id('http://127.0.0.1:5000/')
    for result in results:
        fe = fg.add_entry()
        # print(result['area'])
        fe.id(result['area'] + "/" + str(result['id']))
        fe.title(result['title'])
        if detail:
            fe.content(toxml(result['details']), type='application/xml')
        else:
            fe.content('', type='application/xml')
    result = fg.atom_str(pretty=True)
    return result
