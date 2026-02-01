class MinetestConfParseException(Exception):
    def __init__(self, message=None, cause=None):
        super().__init__(message, cause)

def prepare_conf_for_parsing(conf_file) -> str:
    try:
        with open(conf_file, "r") as f:
            content = f.read()
            curly_braces = 0
            curved_brackets = 0
            cbuf = []
            line_no = 1
            for c in content:
                if c == "\n":
                    line_no += 1

                if c == "{":
                    curly_braces += 1
                elif c == "}":
                    curly_braces -= 1
                elif c == "(":
                    curved_brackets += 1
                elif c == ")":
                    curved_brackets -= 1

                if c == "\n" and (curly_braces != 0 or curved_brackets != 0):
                    continue
                cbuf.append(c)
            if curly_braces != 0:
                raise MinetestConfParseException("Mismatched curly braces")
            if curved_brackets != 0:
                raise MinetestConfParseException("Mismatched curvy brackets")
            return "".join(cbuf)
    except Exception as e:
        if isinstance(e, MinetestConfParseException):
            raise e
        else:
            raise MinetestConfParseException(message=str(e), cause=e)



def iface_handle_tuple(value): pass
def iface_handle_group(value): pass

def handle(value: str):
    if value[0] == "{" and value[-1] == "}":
        value = value[1:-1]
        return iface_handle_group(value)
    elif value[0] == "(" and value[-1] == ")":
        value = value[1:-1]
        return iface_handle_tuple(value)
    elif value[0] == "{" and value[-1] == ")":
        raise MinetestConfParseException("Mismatched Brackets: { vs )")
    elif value[0] == "(" and value[-1] == ")":
        raise MinetestConfParseException("Mismatched Brackets: ( vs }")
    else:
        return value

def iface_handle_tuple(value):
    splitted = value.split(",")
    items = []
    for item in splitted:
        item = item.strip()
        items.append(handle(item))
    return items

def iface_handle_group(value):
    splitted = value.split(",")
    items = {}
    for item in splitted:
        kv = item.split("=", maxsplit=1)
        if len(kv) == 1:
            key = kv[0].strip()
            items[key] = None
        else:
            key, value = kv[0].strip(), kv[1].strip()
            items[key] = handle(value)
    return items

def parse_config(conf_file: str) -> dict:
    try:
        conf_string = prepare_conf_for_parsing(conf_file)
    except MinetestConfParseException as e:
        raise MinetestConfParseException(message="Error in preprocessing caused by :", cause=e)
    config = {}
    for line in conf_string.split("\n"):
        line = line.strip()
        if not line: continue
        if line.startswith("#"): continue
        kv = line.split("=", maxsplit=1)
        if len(kv) == 1:
            key = kv[0].strip()
            config[key] = None
        else:
            key, value = kv[0].strip(), kv[1].strip()
            try:
                config[key] = handle(value)
            except MinetestConfParseException as e:
                raise MinetestConfParseException(message=f"Error at key {key} caused by: ", cause=e)
    return config

