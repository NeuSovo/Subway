FROM python:3.6.6-slim

ENV TZ Asia/Shanghai

WORKDIR /subway

RUN apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends \
        git gcc g++ make default-libmysqlclient-dev && \
    apt-get autoremove -qq -y --purge && \
    rm -rf /var/cache/apt /var/lib/apt/lists

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000