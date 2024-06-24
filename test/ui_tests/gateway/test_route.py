from pages.page_workspaces import Workspaces
from pages.page_workspace import Workspace
from pages.page_gateway_service import GatewayService
from utils.random_util import RandomUtil
import pytest
from ui_tests.base_test.ui_base_test import UIBaseTest
from pages.page_route import Route


class TestRoute(UIBaseTest):

    @pytest.fixture(autouse=True, scope='function')
    def setup_teardown_method(self, init_url_page):
        self.route = Route(self.page)
        self.workspace = Workspace(self.page)
        self.gateway_service = GatewayService(self.page)
        self.route.delete_all_routes(self.base_url)
        self.gateway_service.delete_all_gateway_services(self.base_url)
        yield

    @pytest.mark.golden
    def test_new_route(self):
        self.gateway_service.goto_gateway_service(self.base_url)
        name = f"{RandomUtil.timestamp()}"
        paras = {
            "name": name,
            "url": f"http://kim.org"
        }
        self.gateway_service.new_gateway_service(paras)
        existing = self.route.count_route(self.base_url)
        self.route.goto_routes(self.base_url)
        self.route.new_route(name)
        new = self.route.count_route(self.base_url)
        self.verifier.verify_equals(new, existing + 1)
