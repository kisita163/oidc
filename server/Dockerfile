FROM python:3.6
COPY . /app
ENV CONFIG=2
WORKDIR /app
EXPOSE  7011
RUN pip install -r requirements.txt
CMD ["python", "oidc_rp_server.py"]
