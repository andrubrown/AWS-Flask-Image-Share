import ast
import mimetypes


def save_to_dynamodb(data, ddb_table):
    ddb_table.put_item(data=data)


def query_dynamodb_album(album_id, ddb_table):
    data = ddb_table.get_item(album_id=album_id)
    return ast.literal_eval(data['images'])


def upload_to_s3(file, filename, s3_bucket):
    key = s3_bucket.new_key(filename)
    type = mimetypes.guess_type(filename)
    headers = {'Content-Type': type}
    key.set_contents_from_file(file, headers=headers, replace=True,
                               reduced_redundancy=True, rewind=True)
    key.make_public()
    return key.generate_url(expires_in=0, query_auth=False, force_http=True)
