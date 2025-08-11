import asyncio
import logging

from infra.db.main import get_sa_engine
from infra.log.main import configure_logging
from presentation.api.main import init, run
from settings import settings

logger = logging.getLogger(__name__)


async def async_main() -> None:
    configure_logging(settings=settings.logs)

    logger.info("Launch app")
    app = init()

    async with get_sa_engine(settings.db.asyncurl):
        await run(app)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
