# CCTV Stream Scanner - Educational Tool

⚠️ **IMPORTANT: This tool is for educational purposes only. Use only on networks you own or have explicit permission to test.**

## Description
This tool is designed for educational purposes to help understand network security and the importance of securing IoT devices. It demonstrates how unsecured CCTV cameras can be discovered and accessed, highlighting the need for proper security measures.

## Features
- Network scanning for open RTSP ports
- Default credential testing
- Stream capture and recording
- GUI interface for easy operation
- Detailed logging of all activities

## Prerequisites
- Python 3.8 or higher
- Nmap installed on your system
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd cctv-scanner
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Nmap:
- Windows: Download and install from https://nmap.org/download.html
- Linux: `sudo apt-get install nmap`
- macOS: `brew install nmap`

## Usage

1. Run the tool:
```bash
python cctv_scanner.py
```

2. Enter the network range you want to scan (e.g., 192.168.1.0/24)

3. Click "Start Scan" to begin scanning for cameras

4. Once cameras are discovered, you can:
   - View their details in the table
   - Select a camera and click "Capture Selected Stream" to record its feed

## Security Notes
- Always obtain proper authorization before scanning any network
- Use this tool only for educational purposes
- Respect privacy and data protection laws
- Do not use this tool for malicious purposes

## Logging
All activities are logged to a file named `cctv_scan_YYYYMMDD_HHMMSS.log` in the same directory as the script.

## Disclaimer
This tool is provided for educational purposes only. The authors are not responsible for any misuse or damage caused by this program. Users are responsible for ensuring they have proper authorization before using this tool on any network.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 