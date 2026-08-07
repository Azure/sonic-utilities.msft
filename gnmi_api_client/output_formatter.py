from tabulate import tabulate


EXAMPLE_INTERFACES_STATUS_PATH = "SHOW/interfaces/status"

EXAMPLE_INTERFACES_STATUS_JSON = {
    "interfaces": [
        {
            "Interface": "Ethernet0",
            "Lanes": "0,1,2,3",
            "Speed": "100G",
            "MTU": "9100",
            "FEC": "rs",
            "Alias": "etp1",
            "Admin": "up",
            "Oper": "up",
        },
        {
            "Interface": "Ethernet4",
            "Lanes": "4,5,6,7",
            "Speed": "100G",
            "MTU": "9100",
            "FEC": "rs",
            "Alias": "etp2",
            "Admin": "down",
            "Oper": "down",
        },
    ]
}

_INTERFACES_STATUS_HEADERS = [
    "Interface", "Lanes", "Speed", "MTU", "FEC", "Alias", "Admin", "Oper",
]


class DummyTabularFormatter:
    def format(self, gnmi_path: str, gnmi_json: dict) -> str:
        if gnmi_path != EXAMPLE_INTERFACES_STATUS_PATH:
            raise ValueError(f"no dummy formatter for path {gnmi_path}")

        rows = [
            [entry.get(col, "") for col in _INTERFACES_STATUS_HEADERS]
            for entry in gnmi_json.get("interfaces", [])
        ]
        return tabulate(rows, headers=_INTERFACES_STATUS_HEADERS, tablefmt="simple")
