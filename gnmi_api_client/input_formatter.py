NO_COMMAND_ERROR = "No command provided for conversion"
EMPTY_COMMAND_ERROR = "Empty command"
INVALID_COMMAND_ERROR = "Command must start with 'show'"
NO_PATH_ERROR = "No path segments after 'show'"
SHORT_OPTION_ERROR = "Short options are not supported"
INVALID_OPTION_TOKEN_ERROR = "Invalid option token: --"
INVALID_LONG_OPTION_ERROR = "Invalid long option '--'"


class OptionException(Exception):
    pass


def has_special_char(text: str) -> bool:
    return "=" in text or "]" in text or "[" in text


def escape_gnmi(text: str) -> str:
    # Escape only '/' → '\/'
    return text.replace("/", r"\/")


class ShowCliToGnmiPathConverter:
    def __init__(self, tokens):
        self.tokens = tokens

    def parseLongOption(self, token: str):
        # --flag         -> ('flag', 'True')
        # --key=value    -> ('key',  'value')
        if token == "--":
            raise OptionException(INVALID_OPTION_TOKEN_ERROR)

        body = token[2:]
        if not body:
            raise OptionException(INVALID_LONG_OPTION_ERROR)

        if "=" in body:
            name, value = body.split("=", 1)
            if not name:
                raise OptionException("Invalid long option: missing name before '='")
            if has_special_char(name) or has_special_char(value):
                raise OptionException("Invalid long option: key/value cannot contain =,[,]")
            return name, escape_gnmi(value)

        return body, "True"

    def convert(self) -> str:
        tokens = self.tokens
        if not tokens:
            raise OptionException(EMPTY_COMMAND_ERROR)
        if tokens[0].lower() != "show":
            raise OptionException(INVALID_COMMAND_ERROR)

        tokens = tokens[1:]  # drop 'show'
        out = ["SHOW"]

        for tok in tokens:
            if tok.startswith("-") and not tok.startswith("--"):
                raise OptionException(f"{SHORT_OPTION_ERROR}: '{tok}'")

            if tok.startswith("--"):
                if len(out) == 1:
                    raise ValueError("Option before first path segment")
                key, val = self.parseLongOption(tok)
                out.append(f"[{key}={val}]")
                continue

            if has_special_char(tok):
                raise ValueError("Invalid characters inside of non option")

            out.append("/")
            out.append(escape_gnmi(tok))

        if len(out) == 1:
            raise OptionException(NO_PATH_ERROR)
        return "".join(out)
