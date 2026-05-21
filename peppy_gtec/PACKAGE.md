# Peppy G-TEC Package Structure

This is a properly structured Python package with CLI interface.

## Installing

From the project root directory:

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

## Running

After installation, use the command-line interface:

```bash
# Run with default settings
peppy-gtec

# View help
peppy-gtec --help

# Run with custom options
peppy-gtec --time 60 --no-logo
```

## Package Structure

```
peppy_gtec/
├── __init__.py          # Package initialization and exports
├── core.py              # Core AlwaysGreen class and utilities
└── cli.py               # Command-line interface
```

## Development

To modify the package:

1. Edit code in `peppy_gtec/` modules
2. Test with: `peppy-gtec [options]`
3. Changes are reflected immediately in development mode (`pip install -e .`)

See [README.MD](../README.MD) for full documentation.
