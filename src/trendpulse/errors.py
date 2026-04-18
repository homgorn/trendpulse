class TrendPulseError(Exception):
    code = "TRENDPULSE_ERROR"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(TrendPulseError):
    code = "VALIDATION_ERROR"


class ProviderError(TrendPulseError):
    code = "PROVIDER_ERROR"


class ProviderTimeoutError(ProviderError):
    code = "PROVIDER_TIMEOUT"


class ConfigurationError(TrendPulseError):
    code = "CONFIGURATION_ERROR"
