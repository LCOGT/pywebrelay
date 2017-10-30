FROM python:3.6-alpine
ENV PYWEBRELAY_RELEASE 1.0
RUN pip --no-cache install https://github.com/irasnyd/pywebrelay/archive/${PYWEBRELAY_RELEASE}.zip
CMD /bin/sh
