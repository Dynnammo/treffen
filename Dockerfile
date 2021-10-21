FROM python:3
# Install netcat using it to wait for postgres connection
RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat
# Set workdir
WORKDIR /src
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install python dependencies
RUN pip install --upgrade pip
RUN pip uninstall pytz
RUN pip uninstall zeroconf
RUN pip install pew
RUN pip freeze > requirements.txt
RUN pew new treffen && pew setproject treffen
# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy source code
COPY . .
# Copy docker entrypoint
COPY docker-entrypoint.sh /scripts/
RUN chmod +x /scripts/docker-entrypoint.sh
ENTRYPOINT ["/scripts/docker-entrypoint.sh"]