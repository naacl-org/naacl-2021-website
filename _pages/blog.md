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

Based on the positive reception of the blogs for the NAACL 2018 and COLING 2018 conferences, NAACL-HLT 2019 will also include a blog that will feature posts from various chairs and invited guests and invite readers to comment and share their thoughts. Links to all posts are listed below in chronological order. 

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}