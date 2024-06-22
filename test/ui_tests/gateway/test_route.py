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
        yield

    def test_new_route(self):
        self.gateway_service.goto_gateway_service(self.base_url)
        name = f"{RandomUtil.timestamp()}"
        self.gateway_service.new_gateway_service_by_url(name, "jerry",
                                                        f"http://joy{RandomUtil.timestamp()}.org")

        self.route.goto_routes(self.base_url)
        existing = self.route.count_route()
        self.route.new_route(name)
        new = self.route.count_route()
        self.verifier.verify_equals(new, existing + 1)
