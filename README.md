# Simcenter Flotherm MCP Server

A Model Context Protocol (MCP) Server that enables Claude AI to interact directly with Simcenter Flotherm for thermal simulation workflows.

## Features

- 🔧 **Material Properties Setup** - Configure material parameters for thermal simulation
- 🔥 **Heat Source Configuration** - Define heat generation sources with power and location
- ⚡ **Device Power Configuration** - Set device power consumption and thermal characteristics
- 📊 **Simulation Results Reading** - Extract and read thermal simulation results
- 🤖 **AI-Powered Analysis** - Automatic analysis and interpretation of simulation results using Claude

## Architecture

```
Claude AI
    ↓
MCP Protocol
    ↓
Flotherm MCP Server
    ├── Material Properties Handler
    ├── Heat Source Handler
    ├── Device Power Handler
    ├── Results Reader
    └── Analysis Engine
    ↓
Simcenter Flotherm API/GUI
```

## Installation

### Prerequisites
- Python 3.9+
- Simcenter Flotherm installed on Windows
- Claude API key from Anthropic

### Setup

```bash
# Clone the repository
git clone https://github.com/hungvu7122/Simcenter-Flotherm-XT.git
cd Simcenter-Flotherm-XT

# Install dependencies
pip install -r requirements.txt

# Configure your environment
cp .env.example .env
# Edit .env with your settings
```

## Usage

### Starting the MCP Server

```bash
python src/main.py
```

### Available Tools

#### 1. Setup Material Properties
Configure thermal properties of materials used in simulation.

```json
{
  "tool": "setup_material_properties",
  "parameters": {
    "material_name": "Copper",
    "thermal_conductivity": 400,
    "density": 8960,
    "specific_heat": 385
  }
}
```

#### 2. Configure Heat Sources
Define heat-generating components.

```json
{
  "tool": "configure_heat_source",
  "parameters": {
    "source_name": "CPU",
    "power_watts": 65.5,
    "location": {"x": 50, "y": 50, "z": 10},
    "type": "point_source"
  }
}
```

#### 3. Set Device Power
Configure power consumption for thermal devices.

```json
{
  "tool": "set_device_power",
  "parameters": {
    "device_name": "LED Array",
    "power_watts": 120.0,
    "efficiency": 0.85
  }
}
```

#### 4. Read Simulation Results
Extract thermal simulation output.

```json
{
  "tool": "read_simulation_results",
  "parameters": {
    "simulation_id": "sim_001",
    "result_type": "temperature_field"
  }
}
```

#### 5. Analyze Results
AI-powered analysis of simulation outcomes.

```json
{
  "tool": "analyze_results",
  "parameters": {
    "simulation_id": "sim_001",
    "analysis_type": "thermal_hotspots"
  }
}
```

## Project Structure

```
Simcenter-Flotherm-XT/
├── src/
│   ├── main.py                 # MCP Server entry point
│   ├── server.py               # MCP Server implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── material_handler.py
│   │   ├── heat_source_handler.py
│   │   ├── device_power_handler.py
│   │   ├── results_reader.py
│   │   └── analysis_engine.py
│   ├── flotherm/
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── gui_automation.py
│   │   └── simulation.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_material_handler.py
│   ├── test_heat_source_handler.py
│   └── test_integration.py
├── examples/
│   ├── basic_simulation.py
│   └── advanced_analysis.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Edit `.env` file to configure:

```env
FLOTHERM_INSTALL_PATH=C:\Program Files\Siemens\Simcenter\Flotherm
FLOTHERM_API_PORT=8080
CLAUDE_API_KEY=your_api_key_here
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
```

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Tools

1. Create a new handler in `src/tools/`
2. Implement the handler class
3. Register it in `src/server.py`
4. Add tests in `tests/`

## API Documentation

See [API.md](./API.md) for detailed API reference.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/hungvu7122/Simcenter-Flotherm-XT/issues)
- Documentation: Check the [wiki](https://github.com/hungvu7122/Simcenter-Flotherm-XT/wiki)

## Acknowledgments

- Simcenter Flotherm by Siemens
- Claude AI by Anthropic
- MCP Protocol by Anthropic
