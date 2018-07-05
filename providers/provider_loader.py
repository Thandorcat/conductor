import importlib
import properties

class Provider_Loader:
    def __init__(self, module_name):
        self.module_name = module_name
        module_path = properties.PROVIDERS_DIR + '.' + self.module_name
        self.module = importlib.import_module(module_path)

    def get_provider(self):
        return self.module.Provider()