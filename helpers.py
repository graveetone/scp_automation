from flask import Flask
import yaml
from loguru import logger as loguru_logger
import sys
import paramiko
from scp import SCPClient

LOG_FILE = "log.log"


def get_app_config(app):
    logger = app.logger

    logger.debug("Loading config.yaml config")
    with open("config.yaml") as config:
        return yaml.safe_load(config)


def get_logger():
    loguru_logger.remove()
    loguru_logger.add(sys.stderr, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <b>{message}</b>")
    loguru_logger.add(LOG_FILE, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <b>{message}</b>")

    return loguru_logger


def create_flask_app(name: str):
    app = Flask(name)
    app.logger = get_logger()
    app.config.update(get_app_config(app=app))

    app.logger.debug("Loading SCP client")
    app.config.scp_client = get_scp_client(**app.config["ssh"])

    return app


def get_scp_client(host, port, username, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, password=password)

    return SCPClient(client.get_transport())


def send_file_via_scp(scp_client: SCPClient, filepath: str):
    scp_client.put(filepath, filepath)
