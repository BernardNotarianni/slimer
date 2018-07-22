import pytest
import slimer.ListSerializer


@pytest.fixture
def data():
    return []


def testNullListSerialize(data):
    assert "[000000:]" == slimer.ListSerializer.serialize(data)


def testOneItemListSerialize(data):
    data.append("hello")
    assert "[000001:000005:hello:]" == slimer.ListSerializer.serialize(data)


def testTwoItemListSerialize(data):
    data.append("hello")
    data.append("world")
    assert "[000002:000005:hello:000005:world:]" == slimer.ListSerializer.serialize(data)


def testSerializeNestedList(data):
    sublist = []
    sublist.append("element")
    data.append(sublist)
    assert "[000001:000024:[000001:000007:element:]:]" == slimer.ListSerializer.serialize(data)


def testSerializeListWithNonString(data):
    s = slimer.ListSerializer.serialize([ 1 ])
    #data = ListDeserializer.deserialize(s)
    #assertEquals("1", list.get(0))


def testSerializeNullElement(data):
    data = [ None ]
    s = slimer.ListSerializer.serialize(data);
    assert "[000001:000004:null:]" == s

