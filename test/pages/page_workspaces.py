from .base_page import BasePage


class Workspaces(BasePage):

    def go_to_workspace(self, base_url, workpace_name):
        self.page.goto(base_url)
        workspace = f"//div[@title='{workpace_name}' and @class='workspace-title']/div[@class='workspace-name']"
        self.page.locator(workspace).click()
