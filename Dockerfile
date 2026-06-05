# syntax=docker/dockerfile:1
#
# Manchester United Soccer Culture Project — container image.
#
# Multi-stage build:
#   1. builder  — installs Python deps and renders the static site to dist/.
#   2. runtime  — a small image that re-renders and serves the static site.
#
# Volume handling is deliberately redundant: BOTH the editable Markdown
# source (/app/content) and the generated output (/app/dist) are declared as
# volumes. The entrypoint regenerates dist/ on start, so whether you mount an
# empty named volume over dist/, bind-mount your own content/, or mount
# nothing at all, the served site is always a correct reflection of the
# current content — falling back to the image-baked build if a rebuild fails.

# --------------------------------------------------------------------------
# Stage 1 — builder
# --------------------------------------------------------------------------
FROM ubuntu:24.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip \
    && /opt/venv/bin/python -m pip install -r requirements.txt

COPY . .
RUN /opt/venv/bin/python build_static.py

# --------------------------------------------------------------------------
# Stage 2 — runtime (serves the static site)
# --------------------------------------------------------------------------
FROM ubuntu:24.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    SITE_PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 python3-venv ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Bring the virtualenv and the full project (source + baked build) across.
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Redundant volume mount points: editable content AND generated output.
VOLUME ["/app/content", "/app/dist"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=4s --start-period=5s --retries=3 \
    CMD curl -fsS "http://localhost:${SITE_PORT}/index.html" >/dev/null || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["serve"]

# --------------------------------------------------------------------------
# Stage 3 — static-artifact (export-only target for CI / GitHub Pages)
# `docker build --target static-artifact -o type=local,dest=out .`
# --------------------------------------------------------------------------
FROM scratch AS static-artifact
COPY --from=builder /app/dist /dist
