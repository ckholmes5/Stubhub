import base64

#Establishing some things
app_token = 'fSEW7LLp6IALVacRfWtrie3A14Ma'
consumer_key = 'Z9uXSYyT0RcBC8jmUM3syzRvuXIa'
consumer_secret = 'ilXjFFagiOFVOpfUMrj5vYiJ1ysa'
stubhub_username = 'ckholmes5@gmail.com'
stubhub_password = 'midd2014'

## Generating basic authorization token
combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo)