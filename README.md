Deploying app with high scalability and auto scaling.

Tech stack:
1. cloudformation - automate infrastructure on aws
2. packet - create image
3. chef - configure image
4. elastic load balancer
5. aws autoscaling groups
6. dynamodb - application database
7. nginx - app web server
7. python - automating whole process


Firstly, dynamodb table is created using cloudformation. Autoscaling is enabled for dynamodb.


Using packer ami image is created, with chef as packer provisioner, it installs docker, nginx, application packages and initializes the application such that when the image is booted, the app is ready to respond.


The above created ami id is referenced in cloudformation while hosting the applicatio, this cloudformation script creates a loadbalancer and a aautoscaling group.
The application scales up when the cpu utilization is greater than 90% for a span of 10mins.


When the avove stack creation is complete, a url is provided which serves the web application.

/set?userid=exampleuser&city=examplecity&signupdate=123   - creates a item in table

/get?userid=exampleuser   - gets the exampleuser item



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
python3 deploydb.py --access_key=AKIA6JSSVJNZ5EJ**** --secret_key=ekb+ITApXer7UjJPVNIvQH4JZf5qHxpw6Yp***** --stack_name=stackdb1 --template=djdbcf.yaml

2. build image and copy ami image id
packer build -var 'aws_access_key=AKIA6JSSVJNZ5EJ****' -var 'aws_secret_key=ekb+ITApXer7UjJPVNIvQH4JZf5qHxpw6Y****' djappimage.json

3. deploy app using image id built in step 2
python3 deployapp.py --access_key=AKIA6JSSVJNZ5EJ***** --secret_key=ekb+ITApXer7UjJPVNIvQH4JZf5qHxpw***** --stack_name=stacktest2 --template=djappcf.yaml --ec2keypair=cftest --amiid=ami-0a0efbb8adb05b58b
