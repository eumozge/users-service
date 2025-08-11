from domain.common.exceptions import AppError


class ApplicationError(AppError):
    pass


class RepositoryError(ApplicationError):
    pass


class CommitError(ApplicationError):
    pass


class RollbackError(ApplicationError):
    pass


class MappingError(ApplicationError):
    pass
