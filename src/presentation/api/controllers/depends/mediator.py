from fastapi import Request


def get_mediator(request: Request) -> None:
    return request.app.state.mediator
