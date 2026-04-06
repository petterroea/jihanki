FROM python:3.10-alpine

RUN mkdir -p /srv/jihanki /docker-scratch && \
    addgroup -S jihanki && adduser -S jihanki -G jihanki && \
    chown jihanki:jihanki /srv/jihanki /docker-scratch

WORKDIR /srv/jihanki
COPY . /srv/jihanki

RUN pip install -e .

COPY docker-startup.sh /usr/local/bin/docker-startup.sh
RUN chmod +x /usr/local/bin/docker-startup.sh

USER jihanki
ENTRYPOINT ["docker-startup.sh"]
CMD ["api"]
