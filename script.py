import asyncio
import os
import logging
import argparse
from datetime import datetime
from browser_use import Agent, ChatGoogle, Browser, BrowserProfile
from dotenv import load_dotenv
from pydantic import SecretStr

# Get the absolute path for the log file
script_dir = os.path.dirname(os.path.abspath(__file__))
log_filename = os.path.join(script_dir, 'automation_results.log')

# Setup Logging
# Set up logging
# Console logger for detailed output
logger = logging.getLogger('browser_use')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('INFO     [%(name)s] %(message)s'))
logger.addHandler(console_handler)

# File logger for results only
file_logger = logging.getLogger('results')
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_filename, encoding='utf-8', mode='w')  # 'w' mode to clear file on each run
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
file_logger.addHandler(file_handler)

# Prevent propagation
logger.propagate = False
file_logger.propagate = False
   

# Load environment variables
load_dotenv()

async def main():
    # Add argument parsing
    parser = argparse.ArgumentParser(description="Automate web browsing tasks.")
    parser.add_argument('url', help="The URL to visit and analyze.")
    args = parser.parse_args()
    url_to_check = args.url
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set or .env file not found.")
    
    # Initialize the model with better configuration
    llm = ChatGoogle(
        model='gemini-2.5-flash',
        temperature=0.1  # Lower temperature for more deterministic output
    )

    # Configure browser profile with highlighting and debugging
    profile = BrowserProfile(
        storage_state="cookies.json",
        wait_for_network_idle_page_load_time=5.0,  # Increased wait time
        highlight_elements=True,  # Enable element highlighting
        highlight_clicks=True,  # Highlight clicked elements
        debug=True  # Enable debug mode
    )

    # Create browser with visible window and debugging
    browser = Browser(
        browser_profile=profile,
        headless=False  # Ensure browser is visible
    )

    # Create the agent with the URL from command line
    agent = Agent(
        task=f"""Zadanie: Analiza cen mieszkań na stronie dewelopera

1. Odwiedź stronę: {url_to_check}

2. Cel analizy: Znajdź konkretne ceny mieszkań w ofercie.

3. Kryteria akceptacji cen:
   ✓ Ceny muszą być dokładne (np. '450 000 PLN', '500 000 złotych')
   ✗ NIE akceptuj zakresów cenowych (np. 'ceny od 500 000 PLN')
   ✗ NIE akceptuj wezwań do kontaktu (np. 'zapytaj o cenę', 'wyślij zapytanie', 'skontaktuj się')

4. Gdzie szukać cen:
   - W linkach do konkretnych ofert
   - W tabelach z ofertami
   - W opisach mieszkań
   - W cennikach

5. Format odpowiedzi:
   - Jeśli znaleziono konkretne ceny: 'Dostępne ceny mieszkań'
   - Jeśli nie znaleziono konkretnych cen: 'Brak dostępnych cen mieszkań'

Uwaga: Skupiaj się tylko na konkretnych, jawnie podanych cenach mieszkań.""",
        llm=llm,
        browser=browser
    )

    # Run the agent and get results
    print("\nStarting analysis - browser window should open with highlighted elements...")
    print("Looking for price information - this may take a few moments...")
    
    # Run the agent
    history = await agent.run()
    
    # Add a longer delay to keep the browser window open
    print("\nAnalysis complete - keeping browser window open for 10 seconds to view highlights...")
    await asyncio.sleep(10)
    
    final_result = history.final_result()
    
    # Print and log the results
    # Log the result
    if final_result:
        # Log only the result to file
        file_logger.info(f"URL: {url_to_check} - Result: {final_result}")
        
        # Detailed console output
        logger.info(f"📄 Result: {final_result}")
        logger.info("✅ Task completed")
        logger.info("✅ Successfully")
    else:
        # Log only the result to file
        file_logger.warning(f"URL: {url_to_check} - Result: Brak dostępnych cen mieszkań")
        
        # Detailed console output
        logger.warning("❌ Task failed")

if __name__ == "__main__":
    logger.info("BrowserUse logging setup complete with level info")
    logger.info("Anonymized telemetry enabled. See https://docs.browser-use.com/development/telemetry for more information.")
    print(f"Loading environment variables from: {os.path.abspath(os.path.dirname(__file__))}/.env")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Log file will be saved to: {log_filename}")
    asyncio.run(main())
