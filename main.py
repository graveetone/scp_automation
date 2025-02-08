from flask import render_template, request
from werkzeug.utils import secure_filename
from helpers import create_flask_app, send_file_via_scp
import os

app = create_flask_app(name=__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("main.html")

    fp = request.files["file"]
    filename = secure_filename(fp.filename)

    app.logger.info(f"Saving {filename}")
    fp.save(filename)

    app.logger.info(f"Sending {filename} to remote cluster")
    send_file_via_scp(
        scp_client=app.config.scp_client,
        filepath=filename
    )

    app.logger.info(f"Deleting {filename}")
    os.remove(filename)

    return render_template("main.html", sent_filename=filename)


if __name__ == '__main__':
    app.run()
