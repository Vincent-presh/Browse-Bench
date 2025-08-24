# services/browsebench/agent_tools.py
from typing import List, Dict, Any

class BrowserAgentTools:
    def __init__(self, page):
        """Initializes the agent tools with a Playwright page object."""
        self.page = page

    async def navigate(self, url: str) -> str:
        """Navigates to a given URL."""
        print(f"Navigating to {url}")
        await self.page.goto(url)
        return f"Successfully navigated to {url}"

    async def click(self, selector: str) -> str:
        """Clicks on an element specified by a CSS selector."""
        print(f"Clicking on element: {selector}")
        await self.page.click(selector)
        return f"Successfully clicked on element with selector: {selector}"

    async def type_text(self, selector: str, text: str) -> str:
        """Types text into an input field specified by a CSS selector."""
        print(f"Typing text '{text}' into element: {selector}")
        await self.page.type(selector, text)
        return f"Successfully typed text into element with selector: {selector}"

    async def get_text(self, selector: str) -> str:
        """Gets the text content of an element specified by a CSS selector."""
        print(f"Getting text from element: {selector}")
        return await self.page.text_content(selector)

    async def get_html(self, selector: str = 'body') -> str:
        """Gets the HTML content of an element specified by a CSS selector."""
        print(f"Getting HTML from element: {selector}")
        element = self.page.locator(selector).first
        return await element.inner_html()

    async def scroll(self, direction: str, pixels: int) -> str:
        """Scrolls the page 'up' or 'down' by a specified number of pixels."""
        print(f"Scrolling {direction} by {pixels} pixels")
        await self.page.evaluate(f"window.scrollBy(0, {pixels if direction == 'down' else -pixels})")
        return f"Successfully scrolled {direction} by {pixels} pixels."

    async def wait(self, seconds: int) -> str:
        """Waits for a specified number of seconds."""
        print(f"Waiting for {seconds} seconds")
        await self.page.wait_for_timeout(seconds * 1000)
        return f"Waited for {seconds} seconds."

    async def find_elements(self, selector: str) -> List[Dict[str, Any]]:
        """Finds all elements matching the selector and returns their details."""
        print(f"Finding elements with selector: {selector}")
        elements = self.page.locator(selector)
        count = await elements.count()
        results = []
        for i in range(count):
            element = elements.nth(i)
            tag = await element.evaluate('el => el.tagName')
            results.append({'tag': tag.lower()})
        return results