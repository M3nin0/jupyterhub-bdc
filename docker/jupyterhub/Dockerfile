FROM jupyterhub/jupyterhub:1.0.0

RUN pip install \
    dockerspawner==0.11.1 \
    oauthenticator==0.11

RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/1.0.0/examples/cull-idle/cull_idle_servers.py

COPY jupyterhub_config.py .
