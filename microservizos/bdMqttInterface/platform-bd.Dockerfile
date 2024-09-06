FROM python:3
RUN mkdir /home/inputs
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-build-isolation --no-cache-dir python-csv==0.0.10 paho-mqtt matplotlib pillow pymongo==4.7.2

CMD ["cat", "/etc/os-release"]
