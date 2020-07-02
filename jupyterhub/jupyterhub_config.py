# JupyterHub configuration
# based on: https://github.com/defeo/jupyterhub-docker
#           https://github.com/jupyterhub/jupyterhub-deploy-docker
import os

# CORS
c.NotebookApp.allow_origin = '*'

## Authenticator
# https://oauthenticator.readthedocs.io/en/latest/getting-started.html#gitlab-setup
# http://tljh.jupyter.org/en/latest/howto/auth/google.html
from oauthenticator.google import LocalGoogleOAuthenticator
c.JupyterHub.authenticator_class = LocalGoogleOAuthenticator

c.LocalGoogleOAuthenticator.client_id = os.environ['GOOGLE_CLIENTID']
c.LocalGoogleOAuthenticator.client_secret = os.environ['GOOGLE_CLIENT_SECRET']
c.LocalGoogleOAuthenticator.oauth_callback_url = os.environ['GOOGLE_OAUTH_CALLBACK_URL']

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

## user data persistence
## see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
## ToDo: Define persistence per user
# c.DockerSpawner.volumes = { "jupyterhub-user-{username}": notebook_dir }
c.DockerSpawner.volumes = { os.environ['DATA_VOLUME_CONTAINER']: {"bind": '/home/jovyan/work/shared', "mode": "ro"} }

# Server usage
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '2G'

## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]

# ACL
c.LocalGoogleOAuthenticator.create_system_users = True

c.Authenticator.admin_users = {}
c.Authenticator.whitelist = {}

c.Authenticator.add_user_cmd = ['adduser', '-q', '--gecos', '""', '--disabled-password', '--force-badname']
