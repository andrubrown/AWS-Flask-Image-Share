from flask import render_template, request, send_from_directory, abort, url_for
import flask
import flask_s3
from flask_s3 import FlaskS3
import os
import boto
import config

from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection

from helpers.file_upload_helper import is_file_allowed, get_image_filename
from helpers.submission_helper import get_random_url_string
from helpers.aws_helper import query_dynamodb_album, save_to_dynamodb, upload_to_s3

USE_S3 = True

application = flask.Flask(__name__)
upload_dir = 'user_img'
application.config['LOCAL_UPLOAD_FOLDER'] = upload_dir
application.config['S3_UPLOAD_FOLDER'] = upload_dir
application.config['Photo_Album_Table'] = config.AWS_DYNAMO_TABLE

aws_key_id = config.AWS_ACCESS_KEY_ID
aws_access_key = config.AWS_SECRET_ACCESS_KEY
application.config['AWS_ACCESS_KEY_ID'] = aws_key_id
application.config['AWS_SECRET_ACCESS_KEY'] = aws_access_key
application.config['S3_BUCKET_NAME'] = config.AWS_STORAGE_BUCKET_NAME
application.config.from_envvar('APP_CONFIG', silent=True)

ddb_conn = DynamoDBConnection(
    aws_access_key_id=aws_key_id,
    aws_secret_access_key=aws_access_key
)
ddb_table = Table(application.config['Photo_Album_Table'], connection=ddb_conn)
s3_conn = boto.connect_s3(aws_key_id, aws_access_key)
s3_bucket = s3_conn.create_bucket(config.AWS_STORAGE_BUCKET_NAME)

if USE_S3:
    s3 = FlaskS3()
    s3.init_app(application)
    application.jinja_env.globals.update(url_for=flask_s3.url_for)


@application.route('/')
def main(name=None):
    return render_template('main.html', name=name)


@application.route('/upload', methods=['POST'])
def upload():
    uploaded_images = request.files.getlist('images')

    if any(not is_file_allowed(image) for image in uploaded_images):
        return render_template('submission.html', submission_result='error')

    image_urls = []
    for image in uploaded_images:
        filename = get_image_filename(image)

        if USE_S3:
            s3_dir = application.config['S3_UPLOAD_FOLDER']
            path = os.path.join(s3_dir, filename)
            url = upload_to_s3(image, path, s3_bucket)
        else:
            local_upload_dir = application.config['LOCAL_UPLOAD_FOLDER']
            path = os.path.join(local_upload_dir, filename)
            image.save(path)
            url = url_for('serve_local_image', filename=filename)
        image_urls.append(url)

    page_id = get_random_url_string()
    data = {
        'album_id': page_id,
        'images': str(image_urls)
    }
    save_to_dynamodb(data, ddb_table)
    album_url = url_for('show_album', album_id=page_id, _external=True)
    return render_template('submission.html', album_url=album_url, submission_result='success')


@application.route('/img/<filename>')
def serve_local_image(filename):
    local_upload_dir = application.config['LOCAL_UPLOAD_FOLDER']
    return send_from_directory(local_upload_dir, filename)


@application.route('/i/<album_id>')
def show_album(album_id):
    try:
        image_urls = query_dynamodb_album(album_id, ddb_table)
    except:
        return abort(404)
    return render_template('album.html', image_urls=image_urls, album_id=album_id)


if __name__ == '__main__':
    application.run()
