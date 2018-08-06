---
title: Conference Blog
layout: archive
permalink: /blog/
author_profile: false
sidebar: false
read_time: false
share: true
comments: false
---

{% include base_path %}

Based on the positive reception of the blogs for the NAACL 2018 and COLING 2018 conferences, the NAACL-HLT 2019 website also includes a blog that will feature posts from conference chairs &amp; invited guests. Links to all posts are listed below in chronological order. Each post includes a comment area for readers to share their thoughts. 

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}