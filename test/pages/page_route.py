from .base_page import BasePage
from utils.random_util import RandomUtil
from playwright.sync_api import expect


class Route(BasePage):
    footer_message = "a[class='make-a-wish']"

    def goto_routes(self, base_url, workspace_name="default"):
        url = f"{base_url}/{workspace_name}/routes/"
        self.page.goto(url)
        self.__wait_for_list_to_be_visible()

    def __wait_for_list_to_be_visible(self):
        self.exists(self.page.locator("//div[@class='kong-ui-entities-routes-list']"))

    def __click_new_route(self):
        self.__wait_for_list_to_be_visible()
        buttons = self.page.locator("[data-testid='new-route']")
        if buttons.count() == 0:
            self.page.get_by_test_id("toolbar-add-route").click()
        else:
            self.page.get_by_test_id("new-route").click()
        self.page.wait_for_load_state("load")

    def new_route(self, service_name, path="/", **kwargs):
        self.__click_new_route()
        self.page.get_by_placeholder("Enter a unique name").fill(f"route_{RandomUtil.timestamp()}")
        self.page.get_by_placeholder("Select a service").click()
        self.page.get_by_text(service_name).click()
        self.page.get_by_test_id("route-form-paths-input-1").fill(path)
        self.page.get_by_test_id("form-submit").click()
        self.exists(self.page.locator(Route.footer_message))

    def delete_all_routes(self, base_url, workspace_name="default"):
        self.goto_routes(base_url, workspace_name)
        rows = "//div/table/tbody/tr"
        count = self.page.locator(rows).count()
        if count == 0:
            return
        for i in range(count - 1, -1, -1):
            row = self.page.locator(rows).nth(i)
            name = row.get_attribute("data-testid")
            # click ...
            row.locator("[data-testid='overflow-actions-button']").click()
            # click Delete
            row.locator("//li[@data-testid='action-entity-delete']/button").click()
            # fill in name to confirm delete
            self.page.locator("//input[@data-testid='confirmation-input']").fill(name)
            # click "Yes, delete"
            # self.page.wait_for_load_state("load")
            delete_button = self.page.locator("//button[@data-testid='modal-action-button']")
            expect(delete_button).to_be_enabled(timeout=1000)
            self.page.locator("//button[@data-testid='modal-action-button']").click()
            self.page.on("dialog", self.handle_dialog)

    def count_route(self, base_url, workspace_name="default"):
        self.goto_routes(base_url, workspace_name)
        service_rows = "//div/table/tbody/tr"
        return self.page.locator(service_rows).count()
