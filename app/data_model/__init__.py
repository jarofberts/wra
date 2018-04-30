from abc import ABC, abstractmethod
import datetime


class PrimaryKey(object):
    pass


class HashKey(object):
    pass


class RangeKey(object):
    pass


class DynamoDbBacked(ABC):
    @staticmethod
    @abstractmethod
    def table_def():
        pass


def unpack_typing(obj: type):
    try:
        # Need to grab the outer type
        # noinspection PyProtectedMember
        outer_type = obj._gorg
        return {'type': outer_type, 'of': eval(str(obj).replace(str(outer_type), '').strip('[]'))}
    except AttributeError:
        # Not using typing
        return {'type': obj, 'of': None}
