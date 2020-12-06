import flask
import docker

app = flask.Flask(__name__)
DOCKER_SOCKET = 'unix://var/run/docker.sock'

class ContainerGroup:
    def __init__(self, title, containers):
        self.title = title
        self.containers = containers
        self.up = False

    def update_status(self, running_containers):
        self.up = True
        for c in self.containers:
            c.update_status(running_containers)
            if not c.up:
                self.up = False

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
            if c.name == self.container_name:
                self.status_text = str(c.status)
                if 'running' in self.status_text.lower():
                    self.up = True
                    break

@app.route('/')
def status():
    containers_groups = [ContainerGroup('Basic infrastructure',
                                        [ContainerStatus('Main webserver', 'proxy',
                                                         'Main webserver that acts as entry point before dispatching to other sub-servers'),
                                         ContainerStatus('Docker monitor', 'dockerstatus',
                                                         'Flask webserver, providing this webpage'),
                                         ContainerStatus("Let's encrypt", 'letsencrypt',
                                                         'Companion container for the proxy that automatically installs ssl certificates for other containers'),
                                         ContainerStatus("Dynamic DNS", "dyndns", "Regularly sends updated IP-address changes to the nameserver")
                                         ]),
                         ContainerGroup('Web projects',
                                        [ContainerStatus('Paragliding Weather Scraping', 'paragliding',
                                                         'Simple webscraper that logs hourly weather condition and forecasts + the status of flying/schooling conditions at Hohe Wand.'),
                                         ContainerStatus('VSC monitor', 'vscmonitor',
                                                         'Dashboard that visualizes status and occupation of VSC3 compute nodes'),
                                         ContainerStatus("Static Webserver", "static",
                                                         "Nginx webserver that serves static files for testing at static.myjournal.at")
                                         ]),
                         ContainerGroup('Nextcloud',
                                        [ContainerStatus('Nextcloud', 'nextcloud',
                                                         'Private cloud, providing file storage'),
                                         ContainerStatus('Nextcloud DB', 'nextcloud_db',
                                                         'Database for nextcloud'),
                                         ContainerStatus('Nextcloud cache', 'nextcloud_redis',
                                                         'Redis in-memory cache for accelerating nextcloud')
                                         ]),
                         ContainerGroup('Other cloud services',
                                        [ContainerStatus('Photo Library', 'photoprism',
                                                         'AI powered PhotoPrism gallery of photos, built on top of nextcloud data'),
                                         ContainerStatus('Photo DB', 'photoprism_db',
                                                         'SQL database to power photoprism'),
                                         ContainerStatus('Bitwarden', 'bitwarden', 'Self-hosted password manager')
                                         ])
                         ]

    running_containers = getRunningContainers()
    for cg in containers_groups:
        cg.update_status(running_containers)
    return flask.render_template('dockerstatus.html', container_groups=containers_groups)

def getRunningContainers():
    """Returns a list of the names of running docker containers"""
    client = docker.DockerClient(DOCKER_SOCKET)
    containers = client.containers.list()
    return containers

if __name__ == '__main__':
    # data = getContainerData('data')
    app.run(host="0.0.0.0", port=80)

