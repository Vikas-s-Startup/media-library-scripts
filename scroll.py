import pychrome
import time

# Connect to Chrome DevTools
browser = pychrome.Browser(url="http://127.0.0.1:9232")  # Ensure Chrome is running with --remote-debugging-port=9222

# Get the existing open tab (assuming only one tab is open)
tabs = browser.list_tab()
if not tabs:
    print("No open tabs found!")
    exit(1)

tab = tabs[0]  # Attach to the first open tab

# Enable necessary domains
tab.start()
tab.Network.enable()
tab.Page.enable()
tab.DOM.enable()
tab.Runtime.enable()

print("Scrolling started... Press Ctrl+C to stop.")

try:
    while True:
        # Execute JavaScript to scroll to the bottom
        tab.Runtime.evaluate(expression="window.scrollTo(0, document.body.scrollHeight);")

        # Wait for 3 seconds before scrolling again
        time.sleep(45)

except KeyboardInterrupt:
    print("\nScrolling stopped by user.")

# Gracefully stop the tab
tab.stop()
