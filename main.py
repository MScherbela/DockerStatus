import flask
import os
app = flask.Flask(__name__)
DATA_DIR = 'data'

class ContainerStatus:
    def __init__(self, name, image, description=""):
        self.name = name
        self.image = image
        self.description = description
        self.status_text = ""
        self.up = False

    def update_status(self, container_data):
        for c in container_data:
            if (c['image'] == self.image) and ("up" in c['status'].lower()):
                self.status_text = c['status']
                self.up = True
                break
        else:
            self.status_text = ""
            self.up = False

@app.route('/')
def hello_world():
    containers = [ContainerStatus('Paragliding Weather Scraping', 'paragliding:latest', 'Simple webscraper that logs hourly weather condition and forecasts + the status of flying/schooling conditions at Hohe Wand.'),
                  ContainerStatus('Main webserver', 'nginx_main:latest', 'Main webserver that acts as entry point before dispatching to other sub-servers'),
                  ContainerStatus('Docker monitor', 'dockerstatus:latest', 'Flask webserver, providing this webpage')]
    data = getContainerData(DATA_DIR)
    for c in containers:
        c.update_status(data)
    return flask.render_template('dockerstatus.html', containers=containers)

def getContainerData(data_dir):
    data_rows = []
    with open(os.path.join(data_dir, 'ps.txt')) as f:
        for i,l in enumerate(f):
            if i == 0:
                continue
            data = l.split('  ')
            data = [d.strip() for d in data if len(d)>0]
            data_rows.append(dict(id=data[0], image=data[1], status=data[4]))
    return data_rows

if __name__ == '__main__':
    # data = getContainerData('data')
    app.run(host="0.0.0.0", port=80)

