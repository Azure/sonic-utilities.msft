# Show GNMI Util - JSON to Tabular Format Converter

This package provides formatters to convert JSON output from show commands into tabular CLI format.

## Structure

show_gnmi_util/ 
├── common/              # Common utilities and base classes 
├── formatter/           # Command-specific formatters 
├── scripts/             # Sample JSON files and CLI tool 
└── test/                # Unit tests

## Supported Commands

- `show version`
- `show vlan brief`

## Usage

### Command Line
python show_gnmi_util/scripts/show_arm_cli.py


### In Code
from show_gnmi_util.formatter import ShowVersionFormatter, ShowVlanBriefFormatter
Format show version
formatter = ShowVersionFormatter() output = formatter.format(json_data) print(output)
Format show vlan brief
vlan_formatter = ShowVlanBriefFormatter() vlan_output = vlan_formatter.format(vlan_json_data) print(vlan_output)


## Testing
python -m unittest show_gnmi_util/test/test_formatters.py


## Adding New Formatters

1. Create a new formatter class in `formatter/` directory
2. Extend `BaseFormatter` class
3. Implement the `format()` method
4. Add unit tests in `test/` directory
