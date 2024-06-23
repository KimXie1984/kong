import pytest
import os
from env_config.env_config import EnvConfig
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session', autouse=True)
def env_config():
    if not os.getenv("ENV_NAME"):
        env_name = "local"
    env_config = EnvConfig(env_name)
    yield env_config


@pytest.fixture(scope="class")
def page(env_config):
    with sync_playwright() as pw:
        mode = env_config.mode
        if mode == "headless" or os.getenv("GITHUB_RUN"):
            headless = True
        else:
            headless = False
        if env_config.browser == "chromium":
            browser = pw.chromium.launch(headless=headless, args=["--no-sandbox", "--no-zygote"])
        elif env_config.browser == "firefox":
            browser = pw.firefox.launch(headless=headless)
        else:
            browser = pw.webkit.launch(headless=headless)
        permissions = ["clipboard-read", "clipboard-write"]
        context = browser.new_context(permissions=permissions)
        # 录制日志
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        context.set_default_timeout(10 * 1000)
        page = context.new_page()
        page.goto(env_config.url)
        yield page
        # 保存日志
        context.tracing.stop(
            path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "trace.zip"))
        context.close()
        browser.close()
