import os
from flask import Flask, send_file, request

app = Flask(__name__)


@app.get("/data/<path:path>")
def data_get(path):
    path = os.path.join("data", path)
    filename = path.split("/")[-1]

    if not os.path.exists(path):
        return f"File \"{path}\" not found", 404

    return send_file(
        path_or_file=path,
        as_attachment=True,
        download_name=filename
    )


@app.post("/data/<path:path>")
def data_post(path):
    path = os.path.join("data", path)

    if os.path.exists(path):
        return f"File \"{path}\" already exists", 409

    for _, file in request.files.items():
        os.makedirs(path, exist_ok=True)
        file.save(os.path.join(path, file.filename))

    return f"{len(request.files)} file(s) created", 201


if __name__ == '__main__':
    app.run()
