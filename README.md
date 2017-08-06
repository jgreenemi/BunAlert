## BUN ALERT

Based on XKCD webcomic #1871, this will be an alert system, relying on AWS SNS, to notify subscribers of the existence of a Bun.

### Features
- Subscribe for push notifications on your mobile device for the existence of a Bun.
- Include photo with notification. If not possible, a Bun emoji will suffice.
- Include location coordinates for the Bun, in case subscriber is nearby and wishes to see the Bun.
- Enable scheduled "Do Not Disturb" hours.
- Include Bun rank. This will need to be better defined before implementation.

### Deployment

```
# The initial deployment is done with:
$ zappa deploy dev

# That makes a lot of resources in your AWS account (Lambda, API Gateway, etc.).
# Update it with:
$ zappa update dev
```

### Reference

- [XKCD Webcomic #1682: Bun](https://xkcd.com/1682/)
- [XKCD Webcomic #1871: Bun Alert](https://xkcd.com/1871/)
