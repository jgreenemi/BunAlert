## BUN ALERT

![Bun Alert Logo](https://github.com/jgreenemi/BunAlert/raw/master/static/bunalertlogo.png)

Based on XKCD webcomic #1871, this is an alert system, relying on AWS SNS, to notify subscribers of the existence of a Bun. A live demo is available at:

https://bunalert.jgreenemi.com/

The build details on this project are covered in [the "Bun Alert: An Afternoon XKCD Project" blog post.](https://jgreenemi.com/bun-alert-an-afternoon-xkcd-project/)

### Existing Features

- Subscribe for push notifications on your mobile device for the existence of a Bun. 
- Alerts include a general location description.

### Possible Future Features

- Include photo with notification. If not possible, a Bun emoji will suffice.
- Include location coordinates for the Bun, in case subscriber is nearby and wishes to see the Bun.
- Enable scheduled "Do Not Disturb" hours.
- Include Bun rank. This will need to be better defined before implementation.

### Deployment Notes

Set up your local environment with:

```
$ git clone https://github.com/jgreenemi/BunAlert.git
$ cd BunAlert
$ virtual env
$ source env/bin/activate
(env) $ pip install -r requirements
```

Deploying the package: 

```
$ git clone https://github.com/jgreenemi/BunAlert.git
$ cd BunAlert
$ virtual env
$ source env/bin/activate
(env) $ pip install -r requirements
```

Pushing the code: 

```
# The initial deployment is done with:
$ zappa deploy dev

# That makes a lot of resources in your AWS account (Lambda, API Gateway, etc.).
# Update it with:
$ zappa update dev
```

SNS is used for the PubSub parts of the alert system. The `/subscribe` Flask route handles the subscription of new numbers for the SMS messages to be sent, and `/alert` is used for pushing messages to the SNS Topic. The endpoint for the service is served out by API Gateway, fronting the Lambda function with our code in it. 

### Reference

- [XKCD Webcomic #1682: Bun](https://xkcd.com/1682/)
- [XKCD Webcomic #1871: Bun Alert](https://xkcd.com/1871/)
- [https://www.gun.io/blog/serverless-microservices-with-zappa-and-flask](https://www.gun.io/blog/serverless-microservices-with-zappa-and-flask)
