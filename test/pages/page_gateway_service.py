from .base_page import BasePage
from playwright.sync_api import expect


class GatewayService(BasePage):
    name = "//input[@placeholder='Enter a unique name']"
    tags = "//input[@placeholder='Enter a list of tags separated by comma']"
    url = "//input[@placeholder='Enter a URL']"
    save = "//button[@type='submit']"

    def __wait_for_list_to_be_visible(self):
        self.exists(self.page.locator("//div[@class='kong-ui-entities-gateway-services-list']"))

    def goto_gateway_service(self, base_url, workspace_name="default"):
        url = f"{base_url}/{workspace_name}/services/"
        self.page.goto(url)
        self.__wait_for_list_to_be_visible()

    def __click_add_gateway_service(self):
        self.__wait_for_list_to_be_visible()
        count = self.page.get_by_test_id("new-gateway-service").count()
        if count == 0:
            self.page.get_by_test_id("toolbar-add-gateway-service").click()
        else:
            self.page.get_by_test_id("new-gateway-service").click()

    def new_gateway_service_by_url(self, name, tags, url, **kwargs):
        self.__click_add_gateway_service()
        self.page.locator(GatewayService.name).fill(name)
        self.page.locator(GatewayService.tags).fill(tags)
        self.page.locator(GatewayService.url).fill(url)
        self.page.locator(GatewayService.save).click()
        self.page.wait_for_load_state("load")

    def new_gateway_service_by_separate_elements(self, name, tags, protocol, host, path="", port="8080", **kwargs):
        self.__click_add_gateway_service()
        self.page.locator(GatewayService.name).fill(name)
        self.page.locator(GatewayService.tags).fill(tags)
        # choose to use separate elements
        self.page.get_by_label("Protocol, Host, Port and Path").check()
        self.page.get_by_test_id("gateway-service-protocol-select").click()
        if protocol.startswith("http"):
            self.page.get_by_test_id("select-item-http").get_by_role("button", name=protocol).click()
        elif protocol.startswith("grpc"):
            self.page.get_by_test_id("select-item-grpc").get_by_role("button", name=protocol).click()
        elif protocol.startswith("udp"):
            self.page.get_by_test_id("select-item-udp").get_by_role("button", name=protocol).click()
        elif protocol.startswith("ws"):
            self.page.get_by_test_id("select-item-websocket").get_by_role("button", name=protocol).click()
        else:
            self.page.get_by_test_id("select-item-tcp").get_by_role("button", name=protocol).click()
        self.page.locator("//input[@placeholder='Enter a host']").fill(host)
        path_count = self.page.locator("//input[@placeholder='Enter a path']").count()
        if path_count != 0:
            self.page.locator("//input[@placeholder='Enter a path']").fill(path)
        port_count = self.page.get_by_test_id("gateway-service-port-input").count()
        if port_count != 0:
            self.page.get_by_test_id("gateway-service-port-input").fill(port)
        self.page.locator(GatewayService.save).click()
        self.page.wait_for_load_state("load")

    def delete_all_gateway_services(self, base_url, workspace_name="default"):
        self.goto_gateway_service(base_url, workspace_name)
        service_rows = "//div/table/tbody/tr"
        count = self.page.locator(service_rows).count()
        if count == 0:
            return
        for i in range(count - 1, -1, -1):
            row = self.page.locator(service_rows).nth(i)
            name = row.get_attribute("data-testid")
            # click ...
            row.locator("[data-testid='overflow-actions-button']").click()
            # click Delete
            row.locator("//li[@data-testid='action-entity-delete']/button").click()
            # fill in name to confirm delete
            self.page.locator("//input[@data-testid='confirmation-input']").fill(name)
            # click "Yes, delete"
            delete_button = self.page.locator("//button[@data-testid='modal-action-button']")
            expect(delete_button).to_be_enabled(timeout=1000)
            self.page.locator("//button[@data-testid='modal-action-button']").click()

    def count_gateway_services(self, base_url, workspace_name="default"):
        self.goto_gateway_service(base_url, workspace_name)
        service_rows = "//div/table/tbody/tr"
        return self.page.locator(service_rows).count()
