from app.repositories.mock_exchange_rate_repository import ExchangeRateRepository

repository = ExchangeRateRepository()


class ExchangeRateService:

    def get_exchange_rates(self, base_currency, target_currency=None):
        return repository.get_exchange_rates(base_currency, target_currency)
    