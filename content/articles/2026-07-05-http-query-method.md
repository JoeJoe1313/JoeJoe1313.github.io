---
Title: "QUERY: The HTTP Method We Have Been Faking with POST"
Date: 2026-07-05 07:00
Category: Computer Science
Tags: cs, http, rest, api, fastapi
Slug: http-query-method
Status: published
Redirect: https://medium.com/@levchevajoana/query-the-http-method-we-have-been-faking-with-post-ddd468162c23?sharedUserId=levchevajoana
---

[TOC]

In June 2026 the IETF published [RFC 10008](https://www.rfc-editor.org/rfc/rfc10008.html), which defines a brand new HTTP method: **QUERY**. It is the first new general-purpose method since PATCH ([RFC 5789](https://www.rfc-editor.org/rfc/rfc5789), 2010), and it closes a gap that has existed for as long as HTTP itself: performing a **safe, idempotent** request that carries a **request body**. In this post we look at the method registry as it stands today, what exactly QUERY adds, how it interacts with caching and conditional requests, and what the support story looks like in OpenAPI and FastAPI.
