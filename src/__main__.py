import asyncio
import logging

from di import get_container
from infra.db.main import get_sa_engine
from infra.log.main import configure_logging
from mediator import init_mediator, setup_mediator
from presentation.api.main import init_api, run_api
from settings import settings

logger = logging.getLogger(__name__)


async def async_main() -> None:
    configure_logging(settings=settings.logs)

    logger.info("Launch app")

    async with get_sa_engine(settings.db.asyncurl) as db_engine:
        mediator = init_mediator(di=get_container(db_engine=db_engine))
        setup_mediator(mediator)

        app = init_api(mediator=mediator)

        await run_api(app)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
