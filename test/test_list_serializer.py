import pytest

from slimer.list_serializer import serialize
from slimer.list_serializer import ListSerializer


@pytest.fixture
def data():
    return []


def testNullListSerialize(data):
    assert "[000000:]" == serialize(data)


def testOneItemListSerialize(data):
    data.append("hello")
    assert "[000001:000005:hello:]" == serialize(data)


def testTwoItemListSerialize(data):
    data.append("hello")
    data.append("world")
    assert "[000002:000005:hello:000005:world:]" == serialize(data)


def testSerializeNestedList(data):
    sublist = []
    sublist.append("element")
    data.append(sublist)
    assert "[000001:000024:[000001:000007:element:]:]" == serialize(data)


#def testSerializeListWithNonString(data):
 #   s = ListSerializer.serialize([ 1 ])
    #data = ListDeserializer.deserialize(s)
    #assertEquals("1", list.get(0))


def testSerializeNullElement(data):
    data = [ None ]
    s = serialize(data)
    assert "[000001:000004:null:]" == s
