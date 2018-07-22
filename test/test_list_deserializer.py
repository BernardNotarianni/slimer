import pytest

from slimer.list_serializer import serialize
from slimer.list_deserializer import deserialize
from slimer.list_deserializer import SlimSyntaxError


@pytest.fixture
def data():
    return []

def check(data):
    serialized = serialize(data)
    deserialized = deserialize(serialized)
    assert data == deserialized


def testCantDeseriailzeNullString(data):
    with pytest.raises(SlimSyntaxError):
        deserialize(None)


def testCantDeserializeEmptyString(data):
    with pytest.raises(SlimSyntaxError):
        deserialize('')


def testCantDeserializeStringThatDoesntStartWithBracket(data):
    with pytest.raises(SlimSyntaxError):
        deserialize('hello')


def testCantDeserializeStringThatDoesntEndWithBracket(data):
    with pytest.raises(SlimSyntaxError):
        deserialize('[000000:')


def testEmptyList(data):
    check(data)


def testListWithOneElement(data):
    data.append("hello")
    check(data)


def testListWithTwoElements(data):
    data.append("hello")
    data.append("world")
    check(data)


def testListWithSubList(data):
    sublist = []
    sublist.append("hello")
    sublist.append("world")
    data.append(sublist)
    data.append("single")
    check(data)
