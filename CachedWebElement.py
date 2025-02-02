from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

class CachedWebElement:
    def __init__(self, driver, locator, timeout=30, parent_element=None):
        """
        Initialize the CachedWebElement with a Selenium driver, a locator, and a timeout.
        
        :param driver: Selenium WebDriver instance.
        :param locator: Tuple containing the locator strategy and value (e.g., (By.ID, "element-id")).
        :param timeout: Maximum time to wait for the element to meet conditions (default: 10 seconds).
        :param parent_element: The parent WebElement (if this is a child element).
        """
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self._element = None  # Cached WebElement
        self._parent_element = parent_element  # Parent element for scoped searches

    def _find_element(self):
        """Locate the element using the stored locator and WebDriverWait."""
        try:
            if self._parent_element:
                # If this is a child element, search within the parent element
                return self._parent_element.find_element(*self.locator)
            else:
                # If this is a top-level element, search in the entire DOM
                return WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located(self.locator)
                )
        except TimeoutException:
            raise TimeoutException(f"Element not found with locator: {self.locator}")

    def _refresh_element(self):
        """Refresh the cached element."""
        self._element = self._find_element()

    def _handle_stale_element(self, func, *args, **kwargs):
        """
        Handle stale element exceptions by refreshing the element and retrying the action.
        
        :param func: The method to call on the WebElement.
        :param args: Arguments to pass to the method.
        :param kwargs: Keyword arguments to pass to the method.
        :return: The result of the method call.
        """
        try:
            if self._element is None:
                self._refresh_element()
            return func(self._element, *args, **kwargs)
        except StaleElementReferenceException:
            # If the element is stale, refresh it and retry
            self._refresh_element()
            return func(self._element, *args, **kwargs)

    def click(self):
        """Click the element after ensuring it is clickable."""
        self._handle_stale_element(
            lambda element: WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(element)
            ).click()
        )

    def send_keys(self, text):
        """Send text to the element after ensuring it is visible."""
        self._handle_stale_element(
            lambda element, t: WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of(element)
            ).send_keys(t),
            text
        )

    @property
    def text(self):
        """Get the text content of the element."""
        return self._handle_stale_element(
            lambda element: WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of(element)
            ).text
        )

    def find_element(self, by, value):
        """
        Find a child element within the cached element.
        
        :param by: Locator strategy (e.g., By.ID, By.XPATH).
        :param value: Locator value.
        :return: A new CachedWebElement instance for the child element.
        """
        def _find_child(element):
            return element.find_element(by, value)

        # Find and return a new CachedWebElement for the child element
        return self._handle_stale_element(_find_child)

    def get_attribute(self, name):
        """Get the value of the specified attribute of the element."""
        return self._handle_stale_element(
            lambda element, n: element.get_attribute(n),
            name
        )
    
    def find_elements(self, by, value):
        """
        Find multiple child elements within the cached element.
        
        :param by: Locator strategy (e.g., By.ID, By.XPATH).
        :param value: Locator value.
        :return: A list of WebElement instances for the child elements.
        """
        def _find_children(element):
            return element.find_elements(by, value)
        
        # Ensure the main element is valid and find the child elements
        return self._handle_stale_element(_find_children)