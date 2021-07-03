#!/usr/local/bin/python

import os
import sys

import jinja2


# Utility functions
def log(txt):
    print(txt, file=sys.stderr)


def error(txt):
    log(txt)
    sys.exit(2)


def convert(src, dst, environ):
    """Generate a file from a template
    Args:
        src (str): path to input file
        dst (str): path to file to write
        environ (dict): environment dictionary, for replacement mappings.
    """
    with open(src) as infile:
        template = infile.read()
    rendered = jinja2.Template(template).render(**environ)
    with open(dst, "w") as outfile:
        outfile.write(rendered)


def generate_federation_sender_worker_config(environ,
                                             config_path,
                                             app,
                                             name,
                                             host,
                                             host_port,
                                             port,
                                             server_name):
    listener_resources = []

    volitile_values = {
        "app": app,
        "name": name,
        "host": host,
        "host_port": host_port,
        "port": port,
        "server_name": server_name,
        "listener_resources": listener_resources,
    }

    convert("/templates/synapse_worker.yaml", config_path, volitile_values)
    with open(config_path, 'r') as f:
        for i, line in enumerate(f, start=1):
            print('{} = {}'.format(i, line))

def generate_generic_worker_config(environ,
                                   config_path,
                                   app,
                                   name,
                                   host,
                                   host_port,
                                   port,
                                   server_name):
    listener_resources = ["client", "federation"]

    volitile_values = {
        "app": app,
        "name": name,
        "host": host,
        "host_port": host_port,
        "port": port,
        "server_name": server_name,
        "listener_resources": listener_resources,
    }

    convert("/templates/synapse_worker.yaml", config_path, volitile_values)
    with open(config_path, 'r') as f:
        for i, line in enumerate(f, start=1):
            print('{} = {}'.format(i, line))


def run_create_worker_config(environ, ownership):
    config_dir = environ.get("WORKER_CONFIG_GEN", "/worker-gen")
    name = environ.get("WORKER_NAME")
    if name is None:
        error("""\
Worker name not set
The worker must have a name passed to it via the environment in order
for it to function
""")
    host = environ.get("SYNAPSE_HOST")
    if host is None:
        error("""\
Synapse host not set
The worker must have a the local synapse instance passed to it via the
environment in order for it to function
""")
    host_port = environ.get("SYNAPSE_REPLICATON_PORT", 9093)
    server_name = environ.get("SYNAPSE_HOST_NAME")
    if server_name is None:
        error("""\
Synapse host name not set
The worker must have a the local synapse's hostname passed to it via the
environment in order for it to function
""")
    worker_config = config_dir + "/worker_config.yaml"
    app = environ.get("SYNAPSE_WORKER", "synapse.app.generic_worker")
    port = int(environ.get("WORKER_PORT", 8008))

    if app == "synapse.app.generic_worker":
        generate_generic_worker_config(environ, worker_config,
                                       app, name, host,
                                       host_port, port, server_name)
    elif app == "synapse.app.federation_send"
        generate_federation_sender_worker_config(environ, worker_config,
                                                 app, name, host,
                                                 host_port, port, server_name)
    else:
        error("""\
Synapse worker type is currently not supported or is unknown
These are the workers that are supported:
    synapse.app.generic_worker
    synapse.app.federation_send
""")


def main(args, environ):
    desired_uid = int(environ.get("UID", "991"))
    desired_gid = int(environ.get("GID", "991"))
    if (desired_uid == os.getuid()) and (desired_gid == os.getgid()):
        ownership = None
    else:
        ownership = "{}:{}".format(desired_uid, desired_gid)

    if ownership is None:
        log("Will not perform chmod/gosu as UserID already matches request")

    log("Generating worker config....")
    run_create_worker_config(environ, ownership)


if __name__ == "__main__":
    main(sys.argv, os.environ)
