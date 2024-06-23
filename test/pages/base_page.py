from playwright.sync_api import Page, Dialog
from utils.log_util import logger


class BasePage:
    _uri = None

    def __init__(self, page: Page, uri: str = ''):
        self._uri = uri
        self._page = page

    @property
    def base_url(self):
        return self._page.context._impl_obj._options.get("baseURL")

    @property
    def page(self):
        return self._page

    def open(self, **kwargs):
        # if not self._uri:
        #     todo needs UI exception
        # raise Exception("No uri")
        self.page.goto(self._uri)

    def reload(self, **kwargs):
        self.page.reload(**kwargs)

    def go_back(self, **kwargs):
        self.page.go_back(**kwargs)

    def go_forward(self, **kwargs):
        self.page.go_forward(**kwargs)

    def close(self):
        self.page.close()

    def handle_dialog(self, dialog: Dialog, dismiss=None):
        logger.debug(f"dialog with message {dialog.message}")
        if dismiss:
            dialog.dismiss()
        else:
            dialog.accept()

    def handle_popup(self, popup):
        popup.wait_for_load_state()
        logger.debug(popup.title())

    def exists(self, locator, state="visible", timeout=5 * 1000):
        logger.debug(f"wait for locator to be {state} in {timeout} ms, locator={locator}")
        locator.wait_for(state=state, timeout=timeout)
