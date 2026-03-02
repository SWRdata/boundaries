FROM alpine:3.23

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

# Install tippecanoe
RUN git clone https://github.com/felt/tippecanoe.git
RUN cd tippecanoe
RUN make -j
RUN make install

# Install versatiles-rs
RUN curl -Ls "https://github.com/versatiles-org/versatiles-rs/releases/latest/download/install-unix.sh" | sudo sh

# Install python app
COPY src /app/src
COPY pyproject.toml /app
COPY uv.lock /app

WORKDIR /app

RUN uv sync

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-editable

CMD [".venv/bin/python", "src/main.py"]
