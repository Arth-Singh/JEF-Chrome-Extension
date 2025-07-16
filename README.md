# 0din JEF Tester Chrome Extension

A Chrome extension that provides a graphical interface for the [0din JEF (Jailbreak Evaluation Framework)](https://github.com/0din-ai/0din-JEF) tester. This extension allows security researchers to easily test text content against various jailbreak detection algorithms.

## Features

- **Dark Theme UI** - Matches 0din's official branding
- **Multiple Test Types**:
  - Tiananmen Square Analysis - Detects historical content about 1989 events
  - Nerve Agent Detection - Identifies harmful chemical synthesis instructions
  - Methamphetamine Detection - Analyzes for drug synthesis content
  - Copyright Detection (Harry Potter) - Checks for copyright violations
- **Detailed Results** - Shows scores, percentages, and missing elements
- **Local Execution** - Runs tests locally via native messaging (no data sent to servers)
- **Real-time Testing** - Fast analysis with immediate results

Ie: <img width="501" height="627" alt="image" src="https://github.com/user-attachments/assets/5fa05c88-8013-467e-828d-d634dd6ade2e" />



## Prerequisites

1. **JEF Framework** - You need the 0din JEF framework installed locally
2. **Python Virtual Environment** - JEF should be installed in a virtual environment
3. **Chrome Browser** - For the extension

## Installation

### Step 1: Install JEF Framework

```bash
# Clone the JEF repository
git clone https://github.com/0din-ai/jef.git
cd jef

# Create and activate virtual environment
python3 -m venv jef_env
source jef_env/bin/activate  # On Windows: jef_env\Scripts\activate

# Install JEF
pip install -e .
```

### Step 2: Install the Chrome Extension

1. Download or clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle in the top right)
4. Click "Load unpacked"
5. Select the `0din-Extension` directory
6. Note the Extension ID from the extensions page

### Step 3: Configure Native Messaging

1. Update the extension ID in the native host manifest:
   ```bash
   # Edit the manifest file
   nano native-host/com.odin.jef_tester.json
   
   # Replace "eacemigeeknpobmggdkdeocgobplpfna" with your actual extension ID
   ```

2. Install the native messaging host:
   ```bash
   # Create Chrome's native messaging directory
   mkdir -p ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/
   
   # Copy the manifest (update paths as needed)
   cp native-host/com.odin.jef_tester.json ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/
   ```

3. Update the JEF path in the native host script:
   ```bash
   # Edit native-host/jef_native_host.py
   # Update the jef_path variable to point to your JEF installation
   ```

### Step 4: Verify Installation

1. Click the extension icon in Chrome
2. Paste some test text
3. Select a test type
4. Click "Run Test"
5. You should see results with scores and analysis

## Usage

1. **Enter Text**: Paste or type the text you want to analyze in the text area
2. **Select Test**: Choose from the dropdown menu:
   - Tiananmen Square Analysis
   - Nerve Agent Detection
   - Methamphetamine Detection
   - Copyright (Harry Potter)
3. **Run Test**: Click the "Run Test" button
4. **View Results**: See the score, percentage, and detailed analysis including missing elements

## File Structure

```
0din-Extension/
├── manifest.json              # Chrome extension configuration
├── popup.html                 # Extension popup interface
├── popup.js                   # Frontend JavaScript logic
├── popup.css                  # Dark theme styling
├── background.js              # Service worker for native messaging
├── native-host/               # Native messaging components
│   ├── jef_native_host.py    # Python bridge to JEF
│   └── com.odin.jef_tester.json # Native host manifest
├── icon16.png                 # Extension icons (0din branding)
├── icon48.png
├── icon128.png
└── README.md                  # This file
```

## Troubleshooting

### Extension doesn't appear
- Ensure Developer mode is enabled in Chrome
- Try reloading the extension

### "Native host has exited" error
- Check that JEF is properly installed in the virtual environment
- Verify the native host manifest has the correct extension ID
- Ensure the Python script has execute permissions:
  ```bash
  chmod +x native-host/jef_native_host.py
  ```

### "Failed to communicate with extension" error
- Check the native host manifest is in the correct directory
- Verify all file paths in the configuration are absolute paths
- Check Chrome's console for detailed error messages

### Tests return 0% score
- Ensure you're testing with actual content that contains the elements JEF looks for
- Check that JEF is working correctly by testing it directly in terminal
- Verify the text contains relevant keywords and patterns

## Development

### Adding New Test Types

1. Update the dropdown options in `popup.html`
2. Add command handling in `native-host/jef_native_host.py`
3. Update the parsing logic if the output format differs

### Customizing the Theme

Edit `popup.css` to modify colors, fonts, or layout. The current theme uses:
- Background: `#000000` (black)
- Panels: `#1a1a1a` (dark gray)
- Accent: `#9333ea` (purple)
- Text: `#ffffff` (white)

## Security Considerations

- This extension executes local Python scripts through native messaging
- JEF algorithms run entirely on your local machine
- No data is sent to external servers
- Only use in trusted environments
- The extension requires broad permissions to interface with the local JEF installation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [0din.ai](https://0din.ai) for the JEF framework
- Chrome Extensions API documentation
- Python Native Messaging examples

## Support

For issues related to:
- **JEF Framework**: Visit the [official JEF repository](https://github.com/0din-ai/0din-JEF)
- **This Extension**: Open an issue in this repository
- **0din Platform**: Contact [0din.ai](https://0din.ai)

---

**Note**: This extension is for security research and educational purposes. Users are responsible for ensuring compliance with applicable laws and regulations.
