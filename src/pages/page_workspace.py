from .base_page import BasePage


class Workspace(BasePage):

    def goto_workspace(self, base_url, workspace_name):
        url = f"{base_url}/{workspace_name}/overview/"
        self.page.goto(url)

    def click_gateway_services(self):
        self.page.get_by_role("link", name="Gateway Services").click()

    def click_add_gateway_service(self):
        buttons = self.page.locator("[data-testid='new-gateway-service']")
        if buttons.count() == 0:
            self.page.get_by_test_id("toolbar-add-gateway-service").click()
        else:
            self.page.get_by_test_id("new-gateway-service").click()
