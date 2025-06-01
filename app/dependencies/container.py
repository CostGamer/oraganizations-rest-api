from dishka import make_async_container

from app.dependencies.providers import (
    ConfigsProvider,
    DatabaseConnectionProvider,
    RepoProviders,
    ServiceProviders,
)

container = make_async_container(
    DatabaseConnectionProvider(),
    ConfigsProvider(),
    ServiceProviders(),
    RepoProviders(),
)
