import os
from types import NoneType
from typing import Callable, Any

from dotenv import dotenv_values


class ConfigMeta(type):
    env_attr_key = "env_file"

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        if "Meta" not in attrs:
            raise NotImplementedError(
                f"""Please declare class Meta and set {cls.env_attr_key}. Example:
                \nclass Meta:\n\t{cls.env_attr_key} = '.env'
                """
            )
        meta = attrs["Meta"]
        if not hasattr(meta, cls.env_attr_key):
            raise NotImplementedError(
                f"""Please declare attr env file. Example:
                \nclass Meta:\n\t{cls.env_attr_key} = '.env'
                """
            )
        env_file_path = getattr(meta, cls.env_attr_key)

        env_file_data = dotenv_values(env_file_path)

        all_attrs = attrs | attrs['__annotations__']

        for key, types in all_attrs.items():
            # exclude magic methods
            if key.startswith("__") or key == "Meta":
                continue

            # check exists annotation for field
            if key not in attrs['__annotations__'] and not isinstance(attrs.get(key), Callable):
                raise NotImplementedError(f"Please set annotations for {key}")

            # get annotation types
            try:
                check_types = [t for t in types.__args__]
            except AttributeError:
                check_types = [types]

            # check value from env file or environment
            if (NoneType not in check_types and key not in attrs) and not (
                    env_file_data.get(key) or os.environ.get(key)):
                raise ValueError(f"{key} value required. Please set value!")

            if key in attrs:
                value = attrs[key]

                if isinstance(value, Callable):
                    field_name, value = value(**dict(os.environ.items()), **env_file_data)
                    attrs.update({field_name: value})
                    check_types = [type(value)]
                elif not isinstance(value, str):
                    continue

                # get bool
                if value.lower() in ('true', 'false'):
                    value = True if value.lower() == 'true' else False

                # get float
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                # get int
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass

                if type(value) not in check_types:
                    raise ValueError(
                        "{0} invalid type. Please set value with types {1}! Current value: {2}".format(
                            key, check_types, attrs[key]
                        ))
            else:
                # set new value
                attrs.update({key: env_file_data.get(key)})
        return type(name, bases, attrs)


def make_attr(field_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(**kwargs) -> (str, Any):
            result = func(values=kwargs)
            return field_name, result

        return wrapper

    return decorator
