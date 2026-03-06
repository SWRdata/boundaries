FROM ubuntu:24.04 AS tippecanoe-builder

# Install tippecanoe build deps
RUN apt-get update && apt-get -y install git make gcc g++ libsqlite3-dev zlib1g-dev libcurl4-openssl-dev
RUN git clone --depth 1 https://github.com/felt/tippecanoe.git /tippecanoe-src

WORKDIR /tippecanoe-src
RUN CPPFLAGS="-D__CURL__" LDFLAGS="-lcurl" make -j$(nproc)
RUN make install

FROM ubuntu:24.04

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

# Install tippecanoe runtime deps
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update

RUN apt-get install -y curl libsqlite3-0 zlib1g libcurl4 gdal-bin

COPY --from=tippecanoe-builder /tippecanoe-src/tippecanoe /bin
COPY --from=tippecanoe-builder /tippecanoe-src/tile-join bin/

# Install versatiles-rs
RUN curl -Ls "https://github.com/versatiles-org/versatiles-rs/releases/latest/download/install-unix.sh" | sh

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
