from __future__ import print_function
import boto3
import io
import zipfile
import mimetypes
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    the_zipfile = ''
    portfolio_bucket = s3.Bucket('portfolio.michaelryanitprofessional.net')
    build_bucket = s3.Bucket('portfoliobuild.michaelryanitprofessional.net')
    print ("Bucket: {}" .format(portfolio_bucket.name))
    for obj in portfolio_bucket.objects.all():
      print ("File: {}" .format(obj.key))
    print ("Bucket: {}" .format(build_bucket.name))
    for obj in build_bucket.objects.all():
      the_zipfile = obj.key
      print ("File: {}" .format(obj.key))
    portfolio_bucket.download_file('index.html', 'c:\scratch\labbuild\index.html')
    build_bucket.download_file('portfoliobuild.zip', 'c:\scratch\labbuild\portfoliobuild.zip')
    print ("Uploading contents of zip file |{}|" .format(the_zipfile) )
    print ("  from bucket |{}| created on |{}|" .format(portfolio_bucket.name, portfolio_bucket.creation_date) )
    print ("  to bucket |{}| created on |{}| at |{}|" .format(build_bucket.name, build_bucket.creation_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
    portfolio_zip = io.BytesIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
    with zipfile.ZipFile(portfolio_zip) as myzip:
      for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print("Uploading file: {}" .format(nm))
    print ("Job Complete at: {}" .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    return 'Hello From Lambda'
