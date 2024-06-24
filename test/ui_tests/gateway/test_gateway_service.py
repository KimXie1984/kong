import os.path

from pages.page_workspaces import Workspaces
from pages.page_workspace import Workspace
from pages.page_route import Route
from pages.page_gateway_service import GatewayService
from utils.random_util import RandomUtil
import pytest
from ui_tests.base_test.ui_base_test import UIBaseTest
from utils.yaml_util import YamlUtil
import pytest


class TestGatewayService(UIBaseTest):
    test_data_dir = os.path.join(os.path.dirname(__file__), "data")

    @pytest.fixture(autouse=True, scope='function')
    def setup_teardown_method(self, init_url_page):
        self.workspaces = Workspaces(self.page)
        self.workspace = Workspace(self.page)
        self.gateway_service = GatewayService(self.page)
        self.route = Route(self.page)
        self.route.delete_all_routes(self.base_url)
        self.gateway_service.delete_all_gateway_services(self.base_url)
        self.verifier.verify_equals(GatewayService(self.page).count_gateway_services(self.base_url), 0)
        print(TestGatewayService.test_data_dir)
        yield

    @pytest.mark.smoke
    @pytest.mark.golden
    def test_new_gateway_service(self):
        self.gateway_service.goto_gateway_service(self.base_url)
        paras = {
            "name": f"kim{RandomUtil.timestamp()}",
            "url": f"http://kim.org"
        }
        self.gateway_service.new_gateway_service(paras)
        # TODO simply verify the entity count for now, could validate the entity's attributes with the input in the future
        self.verifier.verify_equals(GatewayService(self.page).count_gateway_services(self.base_url), 1)

    @pytest.mark.smoke
    @pytest.mark.golden
    @pytest.mark.parametrize("paras", YamlUtil.read_yaml(os.path.join(test_data_dir, "new_gateway_service.yaml")))
    def test_new_gateway_service_parameterized(self, paras):
        self.gateway_service.goto_gateway_service(self.base_url)
        self.gateway_service.new_gateway_service(paras)
        # TODO simply verify the entity count for now, could validate the entity's attributes with the input in the future
        self.verifier.verify_equals(GatewayService(self.page).count_gateway_services(self.base_url), 1)

    def test_add_gateway_service_duplicate(self):
        self.gateway_service.goto_gateway_service(self.base_url)
        name = f"kim{RandomUtil.timestamp()}"
        self.gateway_service.new_gateway_service_by_url(name, "kim", f"http://{name}.org")
        self.gateway_service.new_gateway_service_by_url(name, "kim", f"http://{name}.org")
        message = self.page.locator(self.gateway_service.alert_message).text_content()
        self.verifier.verify_in("UNIQUE violation detected", message)
