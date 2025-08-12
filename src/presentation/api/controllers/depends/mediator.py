from fastapi import Request


def get_di(
    request: Request,
) -> None:
    return request.app.state.di


def get_mediator(request: Request) -> None:
    return request.app.state.mediator
