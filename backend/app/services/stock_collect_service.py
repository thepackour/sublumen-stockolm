class StockCollectService:
    """Compatibility service kept intentionally empty.

    KIS reference and market data is never bulk-loaded or persisted. News and
    DART are the only durable external data sources in this application.
    """

    def initialize(self):
        return None
