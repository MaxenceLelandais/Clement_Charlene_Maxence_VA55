import threading

class ConfigService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, properties_file="application.properties"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigService, cls).__new__(cls)
                cls._instance._load(properties_file)
            return cls._instance

    def _load(self, properties_file):
        self._config = {}

        with open(properties_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    self._set_nested(self._config, key.strip().split("."), self._cast(value.strip()))

        # Expose comme attributs Python (config.moteur_droit, etc.)
        for k, v in self._config.items():
            setattr(self, k.replace(".", "_"), v)

    def _set_nested(self, d, keys, value):
        """Construit un dict imbriqué à partir de clés séparées par '.'"""
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    def _cast(self, value):
        """Convertit automatiquement en int ou float si possible"""
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    def get(self, key, default=None):
        return self._config.get(key, default)
