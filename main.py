import flask
import docker
import json

app = flask.Flask(__name__)
DOCKER_SOCKET = 'unix://var/run/docker.sock'

class ContainerGroup:
    def __init__(self, config_dict):
        self.title = config_dict['title']
        self.containers = [ContainerStatus(d) for d in config_dict['containers']]
        self.up = False

    def update_status(self, running_containers):
        self.up = True
        for c in self.containers:
            c.update_status(running_containers)
            if not c.up:
                self.up = False

    def get_as_dict(self):
        return dict(title=self.title,
                    containers=[c.get_as_dict() for c in self.containers])

class ContainerStatus:
    def __init__(self, config_dict):
        self.container_name = config_dict['container_name']
        self.title = config_dict['title']
        self.description = config_dict['description']
        self.status_text = ""
        self.up = False

    def update_status(self, running_containers):
        self.up = False
        self.status_text = ""
        for c in running_containers:
            if c.name == self.container_name:
                self.status_text = str(c.status)
                if 'running' in self.status_text.lower():
                    self.up = True
                    break

    def get_as_dict(self):
        return dict(title=self.title,
                    container_name=self.container_name,
                    description=self.description)

@app.route('/')
def status():
    with open('/config/containers.json') as f:
        container_groups = json.load(f)

    running_containers = getRunningContainers()
    for cg in container_groups:
        cg.update_status(running_containers)
    return flask.render_template('dockerstatus.html', container_groups=container_groups)

def getRunningContainers():
    """Returns a list of the names of running docker containers"""
    client = docker.DockerClient(DOCKER_SOCKET)
    containers = client.containers.list()
    return containers

if __name__ == '__main__':
    pass
