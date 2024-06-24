from .base_page import BasePage
from playwright.sync_api import expect, Page


class GatewayService(BasePage):
    name = "//input[@placeholder='Enter a unique name']"
    tags = "//input[@placeholder='Enter a list of tags separated by comma']"
    url = "//input[@placeholder='Enter a URL']"
    save = "//button[@type='submit']"
    alert_message = ".alert-message"

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

    def new_gateway_service(self, kwargs):
        self.__click_add_gateway_service()
        self.__new_gateway_service_general_info(**kwargs)
        self.__new_gateway_service_endpoint(**kwargs)
        self.__new_gateway_service_advanced_fields(**kwargs)
        self.page.locator(GatewayService.save).click()
        self.page.wait_for_load_state("load")

    def __new_gateway_service_general_info(self, **kwargs):
        name = kwargs.get("name", None)
        if name:
            self.page.locator(GatewayService.name).fill(name)
        tags = kwargs.get("tags", None)
        if tags:
            self.page.locator(GatewayService.tags).fill(tags)

    def __new_gateway_service_endpoint(self, **kwargs):
        url = kwargs.get("url", None)
        if url:
            # choose to use separate elements
            self.page.locator(GatewayService.url).fill(url)
        else:
            # choose to use separate elements
            self.page.get_by_label("Protocol, Host, Port and Path").check()
            protocol = kwargs.get("protocol")
            path = kwargs.get("path", None)
            self.page.get_by_test_id("gateway-service-protocol-select").click()
            if protocol.startswith("http"):
                self.page.get_by_test_id("select-item-http").get_by_role("button", name=protocol).click()
                path_count = self.page.locator("//input[@placeholder='Enter a path']").count()
                assert path_count != 0
                self.page.locator("//input[@placeholder='Enter a path']").fill(path)
            elif protocol.startswith("grpc"):
                self.page.get_by_test_id("select-item-grpc").get_by_role("button", name=protocol).click()
            elif protocol.startswith("udp"):
                self.page.get_by_test_id("select-item-udp").get_by_role("button", name=protocol).click()
            elif protocol.startswith("ws"):
                self.page.get_by_test_id("select-item-websocket").get_by_role("button", name=protocol).click()
                path_count = self.page.locator("//input[@placeholder='Enter a path']").count()
                assert path_count != 0
                self.page.locator("//input[@placeholder='Enter a path']").fill(path)
            else:
                self.page.get_by_test_id("select-item-tcp").get_by_role("button", name=protocol).click()
            host = kwargs.get("host", None)
            port = kwargs.get("port", None)
            self.page.locator("//input[@placeholder='Enter a host']").fill(host)
            self.page.get_by_test_id("gateway-service-port-input").fill(port)

    def __new_gateway_service_advanced_fields(self, **kwargs):
        if kwargs:
            btn_view_advanced_fields = self.page.locator("//button[@data-testid='collapse-trigger-content']")
            btn_view_advanced_fields.click()
        retries = kwargs.get("retries", None)
        if retries:
            self.page.get_by_test_id("gateway-service-retries-input").fill(retries)
        connection_timeout = kwargs.get("connection_timeout", None)
        if connection_timeout:
            self.page.get_by_test_id("gateway-service-connTimeout-input").fill(connection_timeout)
        write_timeout = kwargs.get("write_timeout", None)
        if write_timeout:
            self.page.get_by_test_id("gateway-service-writeTimeout-input").fill(write_timeout)
        read_timeout = kwargs.get("read_timeout", None)
        if read_timeout:
            self.page.get_by_test_id("gateway-service-readTimeout-input").fill(read_timeout)
        client_cert = kwargs.get("client_cert", None)
        if client_cert:
            self.page.get_by_test_id("gateway-service-clientCert-input").fill(client_cert)
        ca_cert = kwargs.get("ca_cert", None)
        if ca_cert:
            self.page.get_by_test_id("gateway-service-ca-certs-input").fill(ca_cert)
        tls_verify = kwargs.get("tls_verify")
        if tls_verify:
            self.page.get_by_test_id("gateway-service-tls-verify-checkbox").check()


class ModelAddGatewayService:
    def __init__(
            self,
            name,
            tags,
            url,
            protocol,
            host,
            path,
            port,
            retries,
            connection_timeout,
            write_timeout,
            read_timeout
    ):
        self.name = name
        self.tags = tags
        self.url = url
        self.protocol = protocol
        self.host = host
        self.path = path
        self.port = port
        self.retries = retries
        self.connection_timeout = connection_timeout
        self.write_timeout = write_timeout
        self.read_timeout = read_timeout
