#!/bin/sh
set -e

case "$1" in
    api)
        exec sanic jihanki.webserver --host=0.0.0.0
        ;;
    worker)
        exec rq worker --with-scheduler --url "${REDIS_URL:-redis://redis}"
        ;;
    *)
        echo "Usage: docker-startup.sh {api|worker}" >&2
        exit 1
        ;;
esac
