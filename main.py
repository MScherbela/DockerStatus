import flask
import os
from datetime import datetime

app = flask.Flask(__name__)
DATA_DIR = '/data'

class ContainerStatus:
    def __init__(self, title, container_name, description=""):
        self.container_name = container_name
        self.title = title
        self.description = description
        self.status_text = ""
        self.up = False

    def update_status(self, container_data):
        for c in container_data:
            if (c['name'] == self.container_name) and ("up" in c['status'].lower()):
                self.status_text = c['status']
                self.up = True
                break
        else:
            self.status_text = ""
            self.up = False

@app.route('/')
def hello_world():
    containers = [ContainerStatus('Paragliding Weather Scraping', 'paragliding', 'Simple webscraper that logs hourly weather condition and forecasts + the status of flying/schooling conditions at Hohe Wand.'),
                  ContainerStatus('Main webserver', 'proxy', 'Main webserver that acts as entry point before dispatching to other sub-servers'),
                  ContainerStatus('Docker monitor', 'dockerstatus', 'Flask webserver, providing this webpage'),
                  ContainerStatus('Who am I?', 'whoami', 'Simple container that exposes its container id via http'),
                  ContainerStatus("Let's encrypt", 'letsencrypt', 'Companion container for the proxy that automatically installs ssl certificates for other containers')]
    data, time = getContainerData(DATA_DIR)
    for c in containers:
        c.update_status(data)
    return flask.render_template('dockerstatus.html', containers=containers, ps_timestamp=str(time))

def getContainerData(data_dir):
    data_rows = []
    time = None
    with open(os.path.join(data_dir, 'ps.txt')) as f:
        for i,l in enumerate(f):
            if i == 0:
                time = datetime.fromisoformat(l.strip())
            else:
                data = l.split(';')
                data = [d.strip() for d in data]
                data_rows.append(dict(id=data[0], name=data[1], status=data[2]))
    return data_rows, time

if __name__ == '__main__':
    # data = getContainerData('data')
    app.run(host="0.0.0.0", port=80)

