# Automated PL Real Estate Developer Website Checker

## Project Context and Purpose

Starting September 11, 2025, following new regulations effective from July 2025, real estate developers in Poland will be legally required to publicly display apartment prices on their websites. This project serves as an automated tool to monitor developers' compliance with these transparency requirements.

### Core Functionality

The script automatically:
- Visits developer websites
- Analyzes content for specific apartment prices
- Distinguishes between actual prices and general price ranges
- Logs results with timestamps
- Generates clear responses: "Available apartment prices" or "No available apartment prices"

### Technology Stack

The project leverages:
- LLM (Large Language Model) for intelligent content analysis
- Browser-Use for browser automation
- Python for process orchestration

---

# Technical Setup Guide

This guide will help you set up the project using the `browser-use` package for web automation with Google's Gemini model.

## Prerequisites

- Python 3.11 or higher
- A Google API key for Gemini model access

## Step-by-Step Setup Guide

### 1. Create and Activate Virtual Environment

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Required Packages

```bash
# Install browser-use and other required packages
pip install browser-use google-generativeai python-dotenv

# Install Playwright package
pip install playwright

# Install Playwright browsers (IMPORTANT: use this exact command)
python -m playwright install chromium --with-deps
```

⚠️ Common Mistake: Don't use `playwright install` directly - it won't work. Always use `python -m playwright install`.

### 3. Set Up Environment Variables

Create a file named `.env` in your project root directory and add your Google API key:

```plaintext
GOOGLE_API_KEY=your_google_api_key_here
```

Replace `your_google_api_key_here` with your actual Google API key.

### 4. Create the Python Script

Create a file named `script.py` with the following content:

```python
import asyncio
from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv

# Read GOOGLE_API_KEY into env
load_dotenv()

# Initialize the model
llm = ChatGoogle(model='gemini-2.5-flash')

async def main():
    # Create agent with the model
    agent = Agent(
        task="Your task description here",  # Replace with your desired task
        llm=llm
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

⚠️ Common Mistakes:
- Make sure to use `async/await` syntax correctly
- Don't forget to wrap your code in an async main function
- Always use `asyncio.run(main())` to run the async function

### 5. Running the Script

The script accepts a developer's website URL as an argument:

```bash
# Make sure your virtual environment is activated
python script.py "https://example-developer.com/"
```

#### Usage Examples

```bash
# Check a single website
python script.py "https://developer-warsaw.com/"

# Example of checking multiple sites using a list
for url in $(cat developer_list.txt); do
    python script.py "$url"
    sleep 5  # Optional delay between requests
done
```

#### Output Format

The script provides output in two forms:

1. **Terminal Output:**
```
Current Working Directory: /path/to/project
Log file will be saved to: /path/to/project/automation_results.log

Final Result: Available apartment prices

Result logged to automation_results.log
```

2. **Log File (`automation_results.log`):**
```
2025-09-11 10:15:23,456 - URL: https://example-developer.com/ - Result: Available apartment prices
2025-09-11 10:20:45,789 - URL: https://another-developer.com/ - Result: No available apartment prices
```

#### Result Interpretation

- `Available apartment prices` - specific apartment prices were found (e.g., "450,000 PLN")
- `No available apartment prices` - no specific prices found or only price ranges are available

#### Compliance Criteria

The script considers prices as "available" only when:
- Specific prices are listed for individual apartments
- Prices are clearly displayed in offers or pricing tables
- Prices are actual values, not ranges or "starting from" prices

The script marks prices as "unavailable" when:
- Only price ranges are shown (e.g., "prices from 500,000 PLN")
- Contact forms are required to get prices
- Prices are hidden behind "contact us" or "send inquiry" buttons

## Troubleshooting

1. **"Command not found: playwright"**
   - Solution: Use `python -m playwright install` instead of `playwright install`

2. **"No module named 'browser_use'"**
   - Solution: Make sure you've activated your virtual environment and installed all packages

3. **"Invalid API key"**
   - Solution: Check that your `.env` file exists and contains the correct API key
   - Make sure the `.env` file is in the same directory as your script

4. **Browser doesn't start**
   - Solution: Make sure you've installed Playwright browsers using the correct command
   - Try running `python -m playwright install chromium --with-deps` again

## Project Structure

Your project directory should look like this:

```
your_project_directory/
├── venv/                  # Virtual environment directory
├── .env                   # Environment variables file
├── script.py             # Your automation script
└── README.md             # This documentation
```

## Additional Notes

- The script will automatically download and configure necessary browser extensions
- The first run might take longer as it sets up the browser environment
- You can modify the `task` parameter in the script to automate different web tasks
- The browser-use package includes built-in privacy features and ad-blocking

## Resources

- [browser-use Documentation](https://docs.browser-use.com)
- [Playwright Python Documentation](https://playwright.dev/python/)
- [Google Gemini API Documentation](https://ai.google.dev/)
