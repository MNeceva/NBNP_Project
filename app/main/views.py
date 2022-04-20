from crypt import methods
from flask import render_template, redirect, url_for, flash, request, send_from_directory, send_file
from flask_login import current_user, login_required
from . import main

from ..models import AudioFiles#, TxtFiles
from .forms import *

from app import app

import os

from werkzeug.utils import secure_filename

def allowed_audio(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_AUDIO_EXTENSIONS"]:
        return True
    else:
        return False


@main.route("/прикачи-запис", methods = ['GET', 'POST'])
@login_required
def upload_files():
    print("I am in upload-filees")
    form = UploadFilesForm()

    try:
        files = AudioFiles.objects(user = current_user)
    except:
        files = {}

    print(len(files))

    if request.method == "POST":
        print(form.audio_file.data)
        if request.files:
            audio = request.files["audio_file"]

            print(f"Audio file: {audio}")

            if audio.filename == "":
                flash("Не постои запис за прикачување!")

            if allowed_audio(audio.filename):
                print("Start saving!\n")
                
                filename = secure_filename(audio.filename)
                print(f"Filename: {filename}")
                path = os.path.join(app.config["UPLOADS_AUDIO_FILES"], filename) #app.config["UPLOADS_AUDIO_FILES"] + "/" + filename

                print(f"Path: {path}")
                

                try:
                    audio_file = AudioFiles.objects(name=filename).get_or_404()
                    flash("Аудио записот кој сакате да го прикачите веќе постои! Oбидете се со друг")
                except:
                    audio.save(path)
                    file_size = os.path.getsize(path)
                    print(f"Size: {file_size} MB")
                    audio_file = AudioFiles(name = filename,
                                            path = path,
                                            format = (filename.rsplit(".", 1)[1]).upper(),
                                            size = file_size/1024,
                                            user = current_user)
                    audio_file.save()
                    
                    flash("Аудио записот е успешно прикачен!")
                
                return redirect(url_for('main.upload_files'))
            else:
                flash("Прикачувањето на запис со моменталната екстензија не е дозволен!")

    return render_template('main/profile.html', form=form, files=files)

@main.route("/превземи-запис", methods=["GET", "POST"])
@login_required
def download_file():
    print("Download files")
    form = UploadFilesForm()

    try:
        files = AudioFiles.objects(user = current_user)
    except:
        files = {}

    if request.form.get("download"):
        filename =  request.form.get('download')
        uploads = app.config['UPLOADS_AUDIO_FILES'] + "/" +filename
        return send_file(uploads, as_attachment=True)


    return render_template('main/profile.html', form=form, files=files)


@main.route("/избриши-запис", methods=["GET", "POST"])
@login_required
def delete_file():
    form = UploadFilesForm()

    try:
        files = AudioFiles.objects(user = current_user)
    except:
        files = {}

    if request.form.get("delete"):
        filename =  request.form.get('delete')
        uploads = app.config['UPLOADS_AUDIO_FILES'] + "/" +filename

        try:
            file = AudioFiles.objects(name=filename).get_or_404()
            file.delete()
            os.remove(uploads)
        except:
            flash("Аудио записот е веќе избришан!")
        
    return render_template('main/profile.html', form=form, files=files)
