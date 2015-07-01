"""Script to upload big files to Amazon S3 Bucket.
   Uses FileChunkIO and MultiPartUpload functionality
   to upload the file. Access credentials are saved in
   the boto config file."""

from __future__ import division
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from boto.s3.key import Key

from filechunkio import FileChunkIO
import os
import math
import traceback

def uploadFile(bucket, filename, chunk_size = 5242880):
    #default chunk_size is 5 MB
    conn = S3Connection()
    b = conn.lookup(bucket)
    if (b is None):
        try:
            b = conn.create_bucket(bucket)
        except S3ResponseError:
            print traceback.print_tb
            return None
            
    mp = b.initiate_multipart_upload(os.path.basename(filename))     #filename is the name of the key
    source_path = os.path.join(filename)
    source_size = os.stat(filename).st_size
    chunk_size = chunk_size
    chunk_count = int(math.ceil(source_size/chunk_size))
    print "Chunk count: %s" % str(chunk_count)
    print "Sending chunks now..."
    for i in range(chunk_count):
        print "Chunk %s" % str(i+1)
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i+1)
    
    try:
        mp.complete_upload()
        key = b.get_key(os.path.basename(filename))
        print key
        return key.generate_url(expires_in=0, method='PUT', query_auth=False)
    except S3ResponseError:
        print traceback.print_tb
        return None
