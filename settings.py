import ujson

class Settings:
    _settings = {}

    @classmethod
    def load(cls, filepath="/sd/appsettings.json"):
        try:
            with open(filepath, "r") as f:
                cls._settings = ujson.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            cls._settings = {}

    @classmethod
    def get(cls, key, default=None):
        return cls._settings.get(key, default)
