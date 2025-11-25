from configs.config import DevelopmentConfig as dev_config
from configs.config import ProductionConfig as prod_config

config = {"development": dev_config, "production": prod_config, "default": dev_config}
