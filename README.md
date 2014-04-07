AWS-Flask-Image-Share
=====================

An image sharing app deployed on AWS Elastic Beanstalk

## Install AWS Elastic Beanstalk

####Linux

```mkdir ~/aws-tools
wget https://s3.amazonaws.com/elasticbeanstalk/cli/AWS-ElasticBeanstalk-CLI-2.6.0.zip
unzip AWS-ElasticBeanstalk-CLI-2.6.0.zip
rm AWS-ElasticBeanstalk-CLI-2.6.0.zip
export PATH=$PATH:~/aws-tools/AWS-ElasticBeanstalk-CLI-2.6.0/eb/linux/python2.7/```

####Mac

```mkdir ~/aws-tools
wget https://s3.amazonaws.com/elasticbeanstalk/cli/AWS-ElasticBeanstalk-CLI-2.6.0.zip
unzip AWS-ElasticBeanstalk-CLI-2.6.0.zip
rm AWS-ElasticBeanstalk-CLI-2.6.0.zip
export PATH=$PATH:~/aws-tools/AWS-ElasticBeanstalk-CLI-2.6.0/eb/macosx/python2.7/```

####Windows

See http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html
Or use the web interface https://console.aws.amazon.com/elasticbeanstalk/home

## Clone this repository

```git clone https://github.com/daeyun/AWS-Flask-Image-Share.git
cd AWS-Flask-Image-Share```

#### Making sure you don't accidentally commit config.py

```git update-index --no-assume-unchanged config.py```

## Configure AWS Elastic Beanstalk

```eb init```

Then enter your AWS Key ID and Access Key. Details here: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html

## Create Application

```eb start```

### View Application

```eb status --verbose```


## Update Application

```git add .
git commit -m "Update app"```

### Deploy

git aws.push
