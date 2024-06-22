from .base_page import BasePage
from utils.random_util import RandomUtil


class Route(BasePage):

    def goto_routes(self, base_url, workspace_name="default"):
        url = f"{base_url}/{workspace_name}/routes/"
        self.page.goto(url)

    def __click_new_route(self):
        buttons = self.page.locator("[data-testid='new-route']")
        if buttons.count() == 0:
            self.page.get_by_test_id("toolbar-add-route").click()
        else:
            self.page.get_by_test_id("new-route").click()

    def new_route(self, service_name, path="/", **kwargs):
        self.__click_new_route()
        self.page.get_by_placeholder("Enter a unique name").fill(f"route_{RandomUtil.timestamp()}")
        self.page.get_by_placeholder("Select a service").click()
        self.page.get_by_text(service_name).click()
        self.page.get_by_test_id("route-form-paths-input-1").fill(path)
        self.page.get_by_test_id("form-submit").click()

    def count_route(self):
        service_rows = "//div/table/tbody/tr"
        return self.page.locator(service_rows).count()
