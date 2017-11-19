Sample serverless framework template to create CloudFront resource that host static web site.


# Install
```
$ npm install -g serverless

$ git clone https://github.com/yKarakita/cfn_cloudfront_example.git

$ cd cfn_cloudfront_example 

$ pip install -r requirements.txt -t vendored
```

Edit `serverless.env.yml`

# Deploy

```
$ serverless deploy
```

Put object to created S3 bucket after deploy, and access CloudFront domain name from your browser.
```buildoutcfg
http://xxxxxxxxxx.cloudfront.net/objectname
```

### References
- https://github.com/y13i/cfn-staticweb-example