# Blog Week 10

### This week's overview

This week we began deploying our s3 website. The initial goal was to be able to use our s3 bucket to be able to hold all of our files and we would be able to use cloud flare to display our website. Things didnt exactly go as planned as we had to use cloudfront in order to be able to have a functional website. One of the issues that I encountered when working on the route 53 configuration for cloudflare is that the CNAME needed to have a weighted policy. When previosuly doing A records I did not get any issue but when using CNAME I had to set this up. Another issue we ran into was that the name servers we had given in the CNAME records did not properly direct traffic to them we were troubled that we could not finish in time so we switched to cloud front. We had to switch the design of the way our diagram and our infrastrucutred worked but we were able to set up our site on time.
