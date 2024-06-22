from .base_page import BasePage


class Workspace(BasePage):

    def goto_workspace(self, base_url, workspace_name):
        url = f"{base_url}/{workspace_name}/overview/"
        self.page.goto(url)

    def click_gateway_services(self):
        self.page.get_by_role("link", name="Gateway Services").click()
