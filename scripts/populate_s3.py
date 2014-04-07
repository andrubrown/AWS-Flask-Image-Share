import flask_s3
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from application import application
import config

application.config['AWS_ACCESS_KEY_ID'] = config.AWS_ACCESS_KEY_ID
application.config['AWS_SECRET_ACCESS_KEY'] = config.AWS_SECRET_ACCESS_KEY
application.config['S3_BUCKET_NAME'] = config.AWS_STORAGE_BUCKET_NAME
s3 = flask_s3.FlaskS3()
s3.init_app(application)
flask_s3.create_all(application)
