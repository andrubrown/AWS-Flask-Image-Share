import imghdr
import hashlib
import base64


def is_file_allowed(file):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return (file and '.' in file.filename and file.filename.rsplit('.', 1)[1]
            in ALLOWED_EXTENSIONS and imghdr.what(file))


def hash_stream(stream, blocksize=65536, max_iterations=10):
    buf = stream.read(blocksize)
    hasher = hashlib.sha256()
    while len(buf) > 0 and max_iterations > 0:
        hasher.update(buf)
        max_iterations -= 1
        buf = stream.read(blocksize)
    stream.seek(0)
    return hasher.digest()


def get_image_filename(image):
    ext = imghdr.what(image)
    checksum = base64.urlsafe_b64encode(hash_stream(image.stream))
    return '.'.join([checksum[:16], ext])
