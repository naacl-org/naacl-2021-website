---
title: "Digital & Collaborative Conference Materials"
author: nitin
author_profile: true
excerpt: "Some thoughts on the the NAACL 2019 conference materials (website, handbook, and app)."
tags:
  website
  app
  whova
  handbook
  survey
categories:
    blog
---

After a successful NAACL 2019, I wanted to take some time to reflect on three important components of the conference-attending experience: the conference website, the conference handbook, and – more recently – the conference app. Having served as the website & app chair for [ACL 2017](http://acl2017.org), [EMNLP 2018](https://emnlp2018.org), and now [NAACL 2019](https://naacl2019.org), I wanted to share some thoughts and (personal) opinions and, hopefully, stimulate some discussion.

### Website 

The conference website is generally ready months before the conference and is constantly updated to communicate crucial logistical and program-related information in the intervening period and during the conference itself. In short, conference websites are primarily information-driven and should not require a redesign every year. Re-using the same design (with appropriate cosmetic changes) is low-maintenance and does not force users to learn new navigational structures. I have tried to follow this practice for the conferences I have been involved in and am pleased to see that it is being continued by the [EMNLP-IJCNLP 2019](https://www.emnlp-ijcnlp2019.org) and the [ACL 2020](https://acl2020.org) website chairs.

An important requirement for re-use is that work done by previous website chairs is well-documented and freely available to fork and adapt. In my opinion, the best way to accomplish this is to use GitHub along with its [Pages](https://pages.github.com) service. The NAACL 2019 website does this, with all of its code and content [entirely open-sourced](https://github.com/naacl-org/naacl-hlt-2019) and extensively documented.

Another important feature of the website is the [detailed conference schedule](https://naacl2019.org/schedule). The NAACL 2019 website uses a responsive, JavaScript-powered schedule page that allows users to not only easily browse the sessions/talks/posters they might be interested in but also select them and generate a PDF of their own customized schedule. Like the rest of the website, the JavaScript schedule code is also [open-sourced](https://github.com/naacl-org/naacl-hlt-2019/blob/gh-pages/assets/js/schedule.js) to promote collaboration and reuse. 

### App

The NAACL 2019 conference app is based on the [Whova](https://whova.com) event management system and judging by what I have heard so far, it was a resounding success. There is also some quantitative information on which to base this impression of the app: [this report](/downloads/whova-app-report.pdf) from Whova about app engagement shows that almost 1500 people downloaded (and, hopefully, used) the app. It also confirms that the Whova social features (community discussion board, direct messaging, easy 1-on-1 meeting scheduling, streamlined exchanging of contact information, etc.) played a very big part in the app's success. We had ~3000 direct messages, ~2500 messages on the community board, and ~600 active participants in community discussions, among other impressive figures.

Since the app was built almost entirely inside the Whova EMS portal, there isn't much code to share but there's still a [repository](https://github.com/naacl-org/naacl-app-2019) with detailed documentation on how to set up various aspects of the app inside the Whova portal.

Like the website, one of the most popular features in the app was the "Agenda" tab which allowed attendees to search and browse sessions and to create customized schedules – almost a 1000 attendees seem to have taken advantage of this feature. What I consider to be an important accomplishment this year is that _both_ the website schedule and the app agenda were generated from a _single source_ and entirely programmatically. This was accomplished with code that parses *ACL-style conference schedule files into an abstract representation and then using that code as a git submodule inside the website and the app repositories. As you might have guessed by now, this parsing code is also entirely [open-sourced](https://github.com/naacl-org/naacl-schedule-2019) and has extensive documentation. 

### Handbook

My remit for NAACL 2019 did not include the printed handbook. Steve DeNeefe took up that challenge and did a great job despite the strict timing constraints and numerous technical and organizational challenges. My thinking on the handbook is the following: I think it's time to end the practice of giving a full printed handbook to every *ACL attendee. Here's my reasoning:

1. Handbooks tend to have a lot of pages (the NAACL one had 305!) – that's a _lot_ of wasted paper after the conference is over.

2. For a majority of attendees, the combination of the conference app and the website provides almost all of the functionality of the handbook.

3. Folks who really want a printed schedule can print out the customized schedule PDF from the website. 

Note that I am not advocating for the abolition of the conference handbook. We can still produce a PDF version, share it on the website a few weeks before the conference, and allow those who really want it to print (parts of) it out themselves. Another option is to only produce a limited number of hard-copies and offer them as additional items for purchase – on a first-come-first-served basis – during registration. 

### Summary

I hope I have made the case for a future where we waste as little of any precious resource as possible when creating our conference materials – whether that resource be the paper used for printing handbooks or the time spent on creating a website or an app from scratch.

If you have any thoughts about about this blog post or about the website & app for NAACL 2019, please feel free to contact me directly. I also strongly encourage you to fill out the [post-conference survey](https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAN__iHODedURTgxQkU5VUs3M1JYSUVZVzZXVUhRTUFITy4u) that was just posted!

I want to end this post by thanking the publication chairs, the handbook chair, the program chairs, and the general chair for all of their amazing help and support during my NAACL 2019 tenure.
