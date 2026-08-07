import argparse
import shlex
import sys

from gnmi_api_client.input_formatter import ShowCliToGnmiPathConverter
from gnmi_api_client.output_formatter import (
    DummyTabularFormatter,
    EXAMPLE_INTERFACES_STATUS_JSON,
    EXAMPLE_INTERFACES_STATUS_PATH,
)


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 50052


class GnmiApiClient:
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, is_test_flag: bool = True):
        self.host = host
        self.port = port
        self.is_test_flag = is_test_flag
        self._output_formatter = DummyTabularFormatter()

    def format_input(self, show_cli_str: str) -> str:
        tokens = shlex.split(show_cli_str)
        return ShowCliToGnmiPathConverter(tokens).convert()

    def get_gnmi_result(self, gnmi_path: str) -> dict:
        if self.is_test_flag:
            if gnmi_path != EXAMPLE_INTERFACES_STATUS_PATH:
                raise NotImplementedError(
                    f"test-mode stub only supports {EXAMPLE_INTERFACES_STATUS_PATH}, got {gnmi_path}"
                )
            return EXAMPLE_INTERFACES_STATUS_JSON

        # Real gNMI transport against f"{self.host}:{self.port}" is not wired up yet.
        raise NotImplementedError(
            f"real gNMI client against {self.host}:{self.port} is not implemented yet"
        )

    def format_output(self, gnmi_path: str, gnmi_json: dict) -> str:
        return self._output_formatter.format(gnmi_path, gnmi_json)

    def run(self, show_cli_str: str) -> str:
        gnmi_path = self.format_input(show_cli_str)
        gnmi_json = self.get_gnmi_result(gnmi_path)
        return self.format_output(gnmi_path, gnmi_json)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a SONiC show CLI command into a gNMI SHOW path, fetch the result, and format it into CLI tabular format."
    )
    parser.add_argument("command", help="show CLI command string, e.g. 'show interfaces status'")
    parser.add_argument("--host", default=DEFAULT_HOST, help="gNMI server host (default: localhost)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="gNMI server port (default: 50052)")
    parser.add_argument(
        "--no-test-flag",
        dest="is_test_flag",
        action="store_false",
        help="disable the hard-coded test fixture and attempt a real gNMI connection",
    )
    parser.set_defaults(is_test_flag=True)
    args = parser.parse_args(argv)

    client = GnmiApiClient(host=args.host, port=args.port, is_test_flag=args.is_test_flag)
    print(client.run(args.command))
    return 0


if __name__ == "__main__":
    sys.exit(main())
