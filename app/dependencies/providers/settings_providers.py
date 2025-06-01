from dishka import Provider, Scope, provide

from app.core.configs.settings import Settings


class ConfigsProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_settings(self) -> Settings:
        return Settings()
