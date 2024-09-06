FROM python:3
RUN mkdir /home/inputs
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-build-isolation --no-cache-dir python-csv==0.0.10 paho-mqtt pandas numpy

CMD ["cat", "/etc/os-release"]
