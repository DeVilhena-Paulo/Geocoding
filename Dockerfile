FROM python:3.8 as build

ENV WORKING_DIR=/app
ENV VIRTUAL_ENV=$WORKING_DIR/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $WORKING_DIR

RUN python3 -m venv $VIRTUAL_ENV

COPY geocoding ./geocoding
COPY requirements.txt .
COPY README.rst .
COPY version.txt .
COPY setup.py .

RUN $VIRTUAL_ENV/bin/pip3 install --no-cache-dir -r requirements.txt
RUN $VIRTUAL_ENV/bin/pip3 install --no-cache-dir .

RUN geocoding download
RUN geocoding decompress
RUN geocoding index
RUN geocoding remove_non_necessary_files


FROM python:3.8 as run

ENV WORKING_DIR=/app
ENV VIRTUAL_ENV=$WORKING_DIR/venv

WORKDIR $WORKING_DIR

COPY --from=build $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=build $WORKING_DIR/version.txt $WORKING_DIR
COPY --from=build $WORKING_DIR/README.rst $WORKING_DIR

ENV PATH=$VIRTUAL_ENV/bin:$PATH

COPY api ./api
COPY site ./site
COPY run.py .
COPY LICENSE .

ARG appPort
RUN echo "PORT = ${appPort}" > api/port.py
EXPOSE ${appPort}

CMD python run.py
