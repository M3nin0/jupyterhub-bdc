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


# Create a new oauthenticator just to normalize the username
class BDCLocalGoogleOAuthenticator(LocalGoogleOAuthenticator):
    def normalize_username(self, username):
        return username.replace("@", "_at_")


c.JupyterHub.authenticator_class = BDCLocalGoogleOAuthenticator

c.LocalGoogleOAuthenticator.client_id = os.environ['GOOGLE_CLIENTID']
c.LocalGoogleOAuthenticator.client_secret = os.environ['GOOGLE_CLIENT_SECRET']
c.LocalGoogleOAuthenticator.oauth_callback_url = os.environ['GOOGLE_OAUTH_CALLBACK_URL']

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.image_whitelist = {
    'ODC:1.8' : 'odc:1.8',
    'R-SITS'  : 'r-sits:1.0'
}
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

## user data persistence
## see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
users_base_dir_source = os.environ.get('USERS_BASE_DIR_SOURCE')
users_base_dir_target = os.environ.get('USERS_BASE_DIR_TARGET')

c.DockerSpawner.notebook_dir = notebook_dir
## ToDo: Define persistence per user
# c.DockerSpawner.volumes = { "jupyterhub-user-{username}": notebook_dir }

data_source= os.environ.get('DATA_SOURCE')
data_target= os.environ.get('DATA_TARGET')
examples_source= os.environ.get('EXAMPLES_SOURCE')
examples_target= os.environ.get('EXAMPLES_TARGET')

c.DockerSpawner.volumes = {
    examples_source : {"bind": examples_target, "mode": "ro"}, 
    data_source: {"bind": data_target, "mode": "ro"}
}

def create_dir_hook(spawner):
    username = spawner.user.name  # get the username
    volume_path = os.path.join(users_base_dir_target, username)
    if not os.path.exists(volume_path):
        os.mkdir(volume_path, 0o755)
    os.chown(volume_path, 1000, 100)
    spawner.volumes[os.path.join(users_base_dir_source, username)] = { "bind": '/home/jovyan/work'}

# attach the hook function to the spawner
c.Spawner.pre_spawn_hook = create_dir_hook

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

c.Authenticator.admin_users = {'vconrado@gmail.com'}
c.Authenticator.whitelist = {'vconrado@gmail.com'}

c.Authenticator.add_user_cmd = ['adduser', '-q', '--gecos', '""', '--disabled-password', '--force-badname']
