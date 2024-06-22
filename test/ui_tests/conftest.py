import pytest
import os
from env_config.env_config import EnvConfig
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope='session', autouse=True)
def base_url():
    if not os.getenv("ENV_NAME"):
        env_name = "local"
    env_config = EnvConfig(env_name)
    yield env_config.url


@pytest.fixture(scope="class")
def page(base_url):
    with sync_playwright() as pw:
        if os.getenv("DOCKER_RUN") or os.getenv("GITHUB_RUN"):
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--no-zygote"], slow_mo=1000)
        else:
            browser = pw.chromium.launch(headless=False, slow_mo=1000)
        permissions = ["clipboard-read", "clipboard-write"]
        context = browser.new_context(permissions=permissions)
        # 录制日志
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.goto(base_url)
        yield page
        # 保存日志
        context.tracing.stop(
            path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "trace.zip"))
        context.close()
        browser.close()
