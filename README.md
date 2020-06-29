# install boto3
sudo apt-get install -y python3-pip
sudo pip3 install boto3

# files desc
deployapp.py - python script to deploy djappcf.yaml cloudformation template
deploydb.py - python script to deploy djdbcf.yaml cloudformation template
djappcf.yaml - cloudformation template for app
djappimage.json - packer image building file, builds ami
djdbcf.yaml - application database cloudformation template


# requirements
1. aws admin keys (aws_access_key and aws_secret_key)
2. ec2 key pair in ap-south-1 region
3. boto3 library


1. deploy db
python3 deploydb.py --access_key=AKIA6JSSVJNZ5EJAFBY2 --secret_key=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 --stack_name=stackdb1 --template=djdbcf.yaml

2. build image and copy ami image id
packer build -var 'aws_access_key=AKIA6JSSVJNZ5EJAFBY2' -var 'aws_secret_key=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' djappimage.json

3. deploy app using image id built in step 2
python3 deployapp.py --access_key=AKIA6JSSVJNZ5EJAFBY2 --secret_key=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 --stack_name=stacktest2 --template=djappcf.yaml --ec2keypair=cftest --amiid=ami-0a0efbb8adb05b58b
