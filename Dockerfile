FROM ghcr.io/prefix-dev/pixi:noble

WORKDIR /app
COPY . .

RUN pixi install --all --locked
RUN rm -rf ~/.cache/rattler
