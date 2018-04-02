from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class StarkConfig(AppConfig):
    name = 'stark'
    def ready(self):
        # print("stark扫描开始.....")
        autodiscover_modules('stark',)
