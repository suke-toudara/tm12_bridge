FROM python:3.10

# Update package list and install certificates
RUN apt-get update && \
    apt-get -y install --no-install-recommends ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --upgrade pip

# Install Basic Packages
COPY ./requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

WORKDIR /workspace