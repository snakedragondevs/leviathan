import os
import re
import time

from logzero import logger

class Config:
    DETECT = -1
    PROPERTIES = 0
    CNF = PROPERTIES
    JSON = 1
    YAML = 2
    SERIALIZED = 4
    ENUM = 5
    ENUMERATION = ENUM

    config = {}
    file = None
    correct = False
    __type = DETECT
    json_options = None
    nested_cache = []
    changed = False

    formats = {
        "properties": PROPERTIES,
        "con": CNF,
        "cnf": CNF,
        "conf": CNF,
        "config": CNF,
        "json": JSON,
        "js": JSON,
        "yml": YAML,
        "yaml": YAML,
        "sl": SERIALIZED,
        "serialize": SERIALIZED,
        "txt": ENUM,
        "list": ENUM,
        "enum": ENUM,
    }

    def __init__(self, file: str, __type: int=DETECT, default=None):
        self.load(file, __type, default)

    def reload(self):
        self.config = {}
        self.nested_cache = []
        self.load(self.file, self.__type)

    def has_changed(self, changed=True) -> None:
        self.changed = changed

    def set_changed(self, changed=True) -> None:
        self.changed = changed

    def fix_yaml_indexes(self, __str: str) -> str:
        return re.sub(r"#^( *)(y|Y|yes|Yes|YES|n|N|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF)( *)\:#m", "\1\"\2\"\3:", __str)

    def load(self, file, __type=DETECT, default=None):
        self.file = file
        self.__type = __type

        if self.__type is self.DETECT:
            extension = os.path.basename(self.file).split(".")
            extension = extension.pop().strip().lower()
            if self.formats[extension]:
                self.__type = self.formats[extension]
            else:
                raise ValueError("Cannot detect config type of ()".format(self.file))

        if not os.path.exists(file):
            self.config: dict = default
            self.save()
        else:
            content = open(file, "r").read()
            if self.__type is self.PROPERTIES:
                self._parse_properties(str(content))  # TODO:
            elif self.__type is self.JSON:
                self.config = None  # TODO:
            elif self.__type is self.YAML:
                content = self.fix_yaml_indexes(content)
                self.config = None #  TODO:
            elif self.__type is self.SERIALIZED:
                self.config = None  # TODO:
            elif self.__type is self.ENUM:
                self.config = None  # TODO:
            else:
                raise ValueError("Config type is unknown")

            # TODO: Fill Defaults

    def save(self) -> None:
        content = None
        if self.__type is self.PROPERTIES:
            content = self._write_properties()
        elif self.__type is self.JSON:
            pass
        elif self.__type is self.YAML:
            pass
        elif self.__type is self.SERIALIZED:
            pass
        elif self.__type is self.ENUM:
            pass
        else:
            raise ValueError("Config type is unknown, has not been set or not detected")

        # TODO: put the contents per file classification
        f = open(self.file, 'w')
        f.write(content)
        f.close()
        self.changed = False

    def set_json_option(self, options: int):
        if self.__type is not self.JSON:
            raise RuntimeError("Attempt to set JSON options for non-JSON config")
        self.json_options = options
        self.changed = True

        return self

    def enable_json_option(self, options: int):
        if self.__type is not self.JSON:
            raise RuntimeError("Attempt to enable  JSON options for non-JSON config")
        self.json_options |= options
        self.changed = True

        return self

    def disable_json_option(self, options: int):
        if self.__type is not self.JSON:
            raise RuntimeError("Attempt to disable JSON options for non-JSON config")
        self.json_options &= ~options
        self.changed = True

        return self

    def get_json_option(self) -> int:
        if self.__type is not self.JSON:
            raise RuntimeError("Attempt to get JSON options for non-JSON config")
        return self.json_options

    def get(self, k, default=False):
        return self.config[k] if self.config[k] else default

    def set(self, k, v=True):
        self.config[k] = v
        self.changed = True
        for nkey, nvalue in self.nested_cache:
            if nkey[0:len(k) + 1] is k + ".":
                del self.nested_cache[nkey]

    def set_all(self, v):
        self.config = v
        self.changed = Trues

    def _write_properties(self) -> str:
        content = "#Properties Config file\r\n#" + time.strftime("%c") + "\r\n"
        for k, v in self.config.items():
            if isinstance(v, bool):
                v = "on" if v else "off"
            elif isinstance(v, list):
                v = ';'.join(v)
            content += str(k) + "=" + str(v) + "\r"
        return content

    def _parse_properties(self, content: str):
        matches = re.findall(r'/([a-zA-Z0-9\-_\.]+)[ \t]*=([^\r\n]*)/u', content)
        if len(matches) > 0:
            for i, k in enumerate(matches[1]):
                v = str(matches[2][i]).strip()
                if v.lower() == "on" or v.lower() == "true" or v.lower() == "yes":
                    v = True
                    break
                if v.lower() == "off" or v.lower() == "false" or v.lower() == "no":
                    v = False
                    break
                if self.config[k]:
                    logger.debug("[Config] Repeated property {} on file {}".format(k, self.file))
                self.config[k] = v