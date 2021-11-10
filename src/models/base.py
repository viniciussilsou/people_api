from typing import Type
from decimal import Decimal
from datetime import datetime, date
from json import loads, dumps, JSONEncoder

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base


class _Base:
    def __init__(self):
        pass

    def to_json(self, null_circular: bool = False) -> dict:
        return loads(
            dumps(
                self,
                cls=new_alchemy_encoder(null_circular=null_circular),
                check_circular=False,
            )
        )

    def to_json_without_ids(self, null_circular: bool = False) -> dict:
        response_dict = loads(
            dumps(
                self,
                cls=new_alchemy_encoder(null_circular=null_circular),
                check_circular=False,
            )
        )
        self.__remove_ids(response_dict)
        return response_dict

    def to_json_without_ids_and_properties(self, props_to_remove: list) -> dict:
        response_dict = loads(
            dumps(self, cls=new_alchemy_encoder(), check_circular=False)
        )
        self.__remove_ids_and_properties(response_dict, props_to_remove)
        return response_dict

    def __remove_ids_and_properties(
        self, input_dict: dict, props_to_remove: list
    ) -> None:
        to_remove = []
        for key, value in input_dict.items():
            if key == "id" or key.endswith("_id") or key in props_to_remove:
                to_remove.append(key)
            if type(value) == dict:
                self.__remove_ids_and_properties(value, props_to_remove)

        for key in to_remove:
            del input_dict[key]

    def __remove_ids(self, input_dict: dict) -> None:
        to_remove = []
        for key, value in input_dict.items():
            if key == "id" or key.endswith("_id"):
                to_remove.append(key)
            if type(value) == dict:
                self.__remove_ids(value)
            elif type(value) == list:
                for item in value:
                    self.__remove_ids(item)

        for key in to_remove:
            del input_dict[key]


Base = declarative_base(cls=_Base)


def new_alchemy_encoder(null_circular: bool = False) -> Type[JSONEncoder]:
    _visited_objs = []

    class AlchemyEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if null_circular:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [
                    x for x in dir(obj) if not x.startswith("_") and x != "metadata"
                ]:

                    value = obj.__getattribute__(field)
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    elif isinstance(value, date):
                        value = str(value)
                    elif isinstance(value, Decimal):
                        value = float(value)

                    if not callable(value):
                        fields[field] = value

                # a json-encodable dict
                return fields

            return JSONEncoder.default(self, obj)

    return AlchemyEncoder