from .base_verifier import BaseVerifier
import pytest
from playwright.sync_api import Page


class UIBaseTest:
    base_url: str
    page: Page
    verifier: BaseVerifier

    @pytest.fixture(autouse=True, scope='function')
    def init_url_page(self, env_config, page):
        self.base_url = env_config.url
        self.page = page
        self.verifier = BaseVerifier()
        yield
