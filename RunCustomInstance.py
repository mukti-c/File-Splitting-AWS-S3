from MultiPartUpload import uploadFile
from datetime import datetime
from boto.ec2 import EC2Connection

def registerCustomImage(bucket, filename):
    # Registers custom image and returns the image id
    start_time = datetime.now()
    print "Starting image upload now: %s" % start_time
    image_loc = uploadFile(bucket, filename, chunk_size=10485760) #Chunk size is 10 MB
    print "Image location: %s" % image_loc
    upload_finished_time = datetime.now()
    print "Uploading image finished at: %s" % upload_finished_time
    
    ec2 = EC2Connection()
    reg_start_time = datetime.now()
    image_id = ec2.register_image(image_location=image_loc)
    register_time = datetime.now()
    print "Finished registering image at: %s" % register_time
    print "Image id = %s" % image_id
    print "Time taken for uploading image: %s" % (upload_finished_time - start_time)
    print "Time taken for registering image: %s" % (register_time - reg_start_time)
    return image_id
    
https://custom-ec2-image.s3.amazonaws.com/261ac7fd-6294-4291-97f9-d3b80d50f9b7.img

