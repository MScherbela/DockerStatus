import flask
import os
from datetime import datetime
import docker

app = flask.Flask(__name__)
DOCKER_SOCKET = 'unix://var/run/docker.sock'

class ContainerStatus:
    def __init__(self, title, container_name, description=""):
        self.container_name = container_name
        self.title = title
        self.description = description
        self.status_text = ""
        self.up = False

    def update_status(self, running_containers):
        self.up = False
        self.status_text = ""
        for c in running_containers:
            if (c.name == self.container_name):
                self.status_text = str(c.status)
                if 'running' in self.status_text.lower():
                    self.up = True
                    break

@app.route('/')
def status():
    target_containers = [ContainerStatus('Paragliding Weather Scraping', 'paragliding', 'Simple webscraper that logs hourly weather condition and forecasts + the status of flying/schooling conditions at Hohe Wand.'),
                         ContainerStatus('Main webserver', 'proxy', 'Main webserver that acts as entry point before dispatching to other sub-servers'),
                         ContainerStatus('Docker monitor', 'dockerstatus', 'Flask webserver, providing this webpage'),
                         ContainerStatus('Who am I?', 'whoami', 'Simple container that exposes its container id via http'),
                         ContainerStatus("Let's encrypt", 'letsencrypt', 'Companion container for the proxy that automatically installs ssl certificates for other containers'),
                         ContainerStatus("VSC3 Monitor", 'vscmonitor', 'Dashboard that visualizes status of VSC3 compute nodes'),
                         ContainerStatus("Static Webserver", "static", "Nginx webserver that serves static files for testing at static.myjournal.at")]
    running_containers = getRunningContainers()
    for c in target_containers:
        c.update_status(running_containers)
    return flask.render_template('dockerstatus.html', containers=target_containers)

def getRunningContainers():
    """Returns a list of the names of running docker containers"""
    client = docker.DockerClient(DOCKER_SOCKET)
    containers = client.containers.list()
    return containers

if __name__ == '__main__':
    # data = getContainerData('data')
    app.run(host="0.0.0.0", port=80)

