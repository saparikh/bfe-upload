FROM python:3.7

# copy python scripts into docker container scripts folder
COPY src/scripts ./scripts/

# copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

# install Python dependencies
RUN python3 -m pip install --upgrade pip
COPY src/requirements.txt ./
RUN python3 -m pip install -r requirements.txt

# make entrypoint script executable
RUN chmod +x /entrypoint.sh

# set entrypoint
ENTRYPOINT ["/entrypoint.sh"]