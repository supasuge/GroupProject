#!/usr/bin/env bash
#
# Container entrypoint for the Manchester United Soccer Culture Project.
#
# Redundant volume handling:
#   * If /app/content is bind-mounted with edited Markdown, we regenerate
#     /app/dist from it on every start.
#   * If /app/dist is an empty named volume mounted over the baked build,
#     the regenerate step repopulates it.
#   * If regeneration fails for any reason, we fall back to whatever build
#     is already present in /app/dist so the container still serves a site.
#
set -euo pipefail

APP_DIR="/app"
DIST_DIR="${APP_DIR}/dist"
PORT="${SITE_PORT:-8000}"

log() { printf '[entrypoint] %s\n' "$*"; }

rebuild_site() {
  log "Regenerating static site from ${APP_DIR}/content ..."
  if (cd "${APP_DIR}" && python build_static.py); then
    log "Static site regenerated into ${DIST_DIR}."
    return 0
  fi
  log "WARNING: rebuild failed."
  return 1
}

ensure_dist() {
  # Try a fresh build first (picks up mounted content / repopulates empty volumes).
  if rebuild_site; then
    return 0
  fi
  # Redundant fallback: serve an existing build if one is present.
  if [ -f "${DIST_DIR}/index.html" ]; then
    log "Falling back to the existing build already present in ${DIST_DIR}."
    return 0
  fi
  log "ERROR: no usable build available and rebuild failed."
  return 1
}

case "${1:-serve}" in
  serve)
    ensure_dist
    log "Serving ${DIST_DIR} on 0.0.0.0:${PORT}"
    exec python -m http.server "${PORT}" --directory "${DIST_DIR}" --bind 0.0.0.0
    ;;
  build)
    rebuild_site
    log "Build complete. Output in ${DIST_DIR}."
    ;;
  *)
    # Allow running arbitrary commands (e.g. a shell) for debugging.
    exec "$@"
    ;;
esac
