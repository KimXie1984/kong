import configparser
import os
import logging


class EnvConfig:
    def __init__(self, env_name, conf_file="default_env.ini"):
        self._conf = configparser.ConfigParser()
        self.env_config_dir = os.path.dirname(__file__)
        self._conf_file = os.path.join(self.env_config_dir, conf_file)
        self._conf.read(self._conf_file, encoding="utf-8")

        self.logger = logging.getLogger("UIAutoTest")
        self._env_name = env_name

    @property
    def conf(self):
        return self._conf

    @property
    def url(self):
        return self._conf.get(self.env_name, "url")

    @property
    def browser(self):
        return self._conf.get(self.env_name, "browser")

    @property
    def mode(self):
        return self._conf.get(self.env_name, "mode")


    @property
    def env(self):
        """
        :return: opts of testing|local|...
        """
        return self._conf.options(self.env_name)

    @property
    def env_name(self):
        return self._env_name


def get_env_config(test_env) -> EnvConfig:
    return EnvConfig(env_name=test_env)
