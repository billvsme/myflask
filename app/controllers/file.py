# coding: utf-8
import os
from PIL import Image
from flask import g, request, current_app, send_from_directory, Blueprint


file_bp = Blueprint('file', __name__)


@file_bp.route("/<path:path>")
def file(path):
    if request.args.get('w'):
        w = int(request.args['w'])
        if path.rsplit('.', 1)[1].lower() in ['jpg', "jpeg", "png"]:
            t = path.rsplit('.', 1)
            t[0] += f"_w_{w}"
            thumbnail_path = ".".join(t)
            thumbnail_file_path = os.path.join(
                current_app.config["FILE_FOLDER"], thumbnail_path)

            if not os.path.exists(thumbnail_file_path):
                im = Image.open(os.path.join(current_app.config["FILE_FOLDER"], path))
                im.thumbnail((w, w))
                im.save(thumbnail_file_path)

            path = thumbnail_path

    print(current_app.config["FILE_FOLDER"])
    return send_from_directory(current_app.config["FILE_FOLDER"], path)
