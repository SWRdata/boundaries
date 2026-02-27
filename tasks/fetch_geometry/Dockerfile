FROM debian:12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE="only-managed"

RUN uv python install 3.12

WORKDIR /app
COPY src /app/src
COPY data-swr-de-chain.pem /app
COPY pyproject.toml /app
COPY uv.lock /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-editable

# ==========================================================

FROM gcr.io/distroless/cc-debian12

COPY --from=builder /python /python
COPY --from=builder /app /app

WORKDIR /app
CMD [".venv/bin/python", "src/main.py"]
