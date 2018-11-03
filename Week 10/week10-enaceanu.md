+++
title = "Alex's Blog. Week 10."
description = "SAPS Project"
tags = [
    "Blog",
    "beats",
    "Alex",
    "COMP 480",
    "Project 5",
    "SAPS",
]
date = "2018-11-02"
categories = [
    "Blog",
]
+++

#### Project 5
It is now week 10 and we have done 6 projects as a team, projects 0-5. For project 5, we had to implement the previous project, which was all about the cheapest way to host a blog. The intent was to go without the use of instances. This would serve as a simple way to help save money. The blog site would be a collection of files in an S3 bucket, not a web server(s) which would be running constantly to deliver content. The challenge then would be to lower the cost of site requests. This was accomplished with a service known as Cloudflare.

Cloudfare is a U.S. based company that provides content delivery network services, DDoS mitigation, Internet security and distributed DNS services. It is interesting to note the robustness of this service and the implications of potential with regards to scalability. For our purposes, we only needed content delivery services due to the relative simplicity of our site. Cloudflare will cache our web pages so the S3 bucket will not have to be accessed as often, thereby reducing costs.

#### Student Academic Progression System (SAPS)
Last week we had presentations and SAPS was one f them. I chose the team and ended up working on the project. I think it will be an interesting experience. It will be technical and tactical. Technical as in all the infrastructure and code that will be required, and tactical since we will be working with essentially 3 groups of students. This project has been going on since last semester, and the fruits of the prior students labor are in production as a successful permission number request system website. The Information Systems (IS) team is a continuation of last semester (although with all new members) recruited by the IS department. So that is 1 group, that has a lead who acts as project manager. The second team would be computer science senior design students and the third CIT senior design students. It is possible that the CIT and CS teams will work as one or be viewed as one by the IS team. I think this is where the communication aspect of working on an endeavor like this is going to be crucial. We will see how things go this Monday at our first meeting with all teams.
