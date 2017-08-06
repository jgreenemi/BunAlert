## BUN ALERT

Based on XKCD webcomic #1871, this is an alert system, relying on AWS SNS, to notify subscribers of the existence of a Bun.

### Existing Features

- Subscribe for push notifications on your mobile device for the existence of a Bun. 
- Alerts include a general location description.

### Planned Features

- Include photo with notification. If not possible, a Bun emoji will suffice.
- Include location coordinates for the Bun, in case subscriber is nearby and wishes to see the Bun.
- Enable scheduled "Do Not Disturb" hours.
- Include Bun rank. This will need to be better defined before implementation.

### Deployment Notes

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