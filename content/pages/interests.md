---
Title: Interests
jinja: true
---

Books I am currently reading, and books I find interesting.

{% if goodreads_activity is defined %}
{% include 'goodreads_activity.html' %}
{% endif %}

{% if goodreads_quotes is defined %}
{% include 'goodreads_quotes.html' %}
{% endif %}
