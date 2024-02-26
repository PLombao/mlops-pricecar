FROM python:3.10-slim

COPY config/requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y git && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# INSTALL LIBRARY modelbuilder
COPY config/modelbuilder-0.3.1.tar.gz modelbuilder-0.3.1.tar.gz
RUN pip install modelbuilder-0.3.1.tar.gz

COPY config/ config/
COPY api/ /api/
COPY run_api.py run_api.py

EXPOSE 8000

ENTRYPOINT ["python", "run_api.py"]