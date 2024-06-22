from pages.page_workspaces import Workspaces
from pages.page_workspace import Workspace
from pages.page_gateway_service import GatewayService
from utils.random_util import RandomUtil
import pytest
from ui_tests.base_test.ui_base_test import UIBaseTest


class TestGatewayService(UIBaseTest):

    @pytest.fixture(autouse=True, scope='function')
    def clean_gateway_services(self, init_url_page):
        GatewayService(self.page).clean_gateway_services(self.base_url)
        self.verifier.verify_equals(GatewayService(self.page).count_gateway_services(), 0)
        yield

    def test_new_gateway_service(self):
        Workspaces(self.page).go_to_workspace(self.base_url, "default")
        Workspace(self.page).click_gateway_services()
        Workspace(self.page).click_add_gateway_service()
        GatewayService(self.page).new_gateway_service_by_url(f"{RandomUtil.timestamp()}", "jerry",
                                                             f"http://joy{RandomUtil.timestamp()}.org")
        self.verifier.verify_equals(GatewayService(self.page).count_gateway_services(), 1)
        Workspace(self.page).click_add_gateway_service()
        GatewayService(self.page).new_gateway_service_by_separate_elements(f"{RandomUtil.timestamp()}", "jerry", "grpc",
                                                                           "baidu.com", "", "")
        self.verifier.verify_equals(GatewayService(self.page).count_gateway_services(), 2)
