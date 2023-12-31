import settings
from src.workers.consumers.runner import application, bootstrap


config = settings.ConsumersConfig(
    loyalty_api_client=settings.LOYALTY_API_SERVICE,
    calculation_of_points_consumer=settings.CALCULATION_OF_POINTS_CONSUMER,
    calculation_of_points_amqp_sender=settings.CALCULATION_OF_POINTS_SENDER,
    deposit_points_consumer=settings.DEPOSIT_POINTS_CONSUMER,
)

resources = bootstrap.resolve_resources(config=config)

resources.register(application.Runner)

consumers = resources.resolve(application.Runner).consumers
