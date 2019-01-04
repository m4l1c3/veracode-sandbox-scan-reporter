FROM alpine:latest
RUN apk add build-base python3-dev libffi-dev openssl-dev
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip
RUN pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

RUN addgroup -S scanreport && adduser -S -H -D -s /bin/false scanreport -G scanreport
RUN touch /var/log/cron.log
RUN rm -r /root/.cache
RUN mkdir /setup
COPY ./app/requirements.txt /setup/requirements.txt
RUN cd /setup && \
    python -m pip install -r requirements.txt && \
    rm -rf /setup

COPY ./src /src
COPY app/run.sh /run.sh
COPY app/proc.sh /proc.sh
COPY app/sandbox_report_cron /etc/periodic/daily/sandbox_report_cron
RUN chown -R scanreport.scanreport /src && \
    chown -R scanreport.scanreport /run.sh && \
    chown -R scanreport.scanreport /proc.sh && \
    chmod a+x /etc/periodic/daily/sandbox_report_cron && \
    chmod a+x /run.sh && \
    chmod a+x /proc.sh

ENTRYPOINT ["/run.sh"]

