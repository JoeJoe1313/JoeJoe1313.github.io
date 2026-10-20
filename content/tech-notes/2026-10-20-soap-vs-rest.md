---
Title: SOAP vs. REST
Date: 2026-10-20 07:00
Category: Computer Science
Tags: cs, api, http, soap, rest, tech-notes
Slug: soap-vs-rest
Status: published
---

**SOAP is a messaging protocol; REST is an architectural style.** SOAP specifies how to structure and process messages. REST (Representational State Transfer) describes how components interact through resources and their representations. Both can support an API, but they define different aspects of its design. See the [SOAP messaging framework](https://www.w3.org/TR/soap12-part1/) and [Fielding's definition of REST](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm).

## The same task, two interfaces

Suppose a client needs the status of order `42`. The following examples show illustrative exchanges over HTTPS; routine HTTP headers are omitted.

### SOAP: send a structured message

A SOAP service might expose an operation called `GetOrder`. The client sends a **SOAP 1.2** message to the service endpoint:

```http
POST /OrderService HTTP/1.1
Host: api.example.com
Content-Type: application/soap+xml; charset=utf-8

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
               xmlns:ord="https://example.com/orders">
  <soap:Body>
    <ord:GetOrder>
      <ord:Id>42</ord:Id>
    </ord:GetOrder>
  </soap:Body>
</soap:Envelope>
```

The response also uses a SOAP envelope:

```http
HTTP/1.1 200 OK
Content-Type: application/soap+xml; charset=utf-8

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
               xmlns:ord="https://example.com/orders">
  <soap:Body>
    <ord:GetOrderResponse>
      <ord:Id>42</ord:Id>
      <ord:Status>shipped</ord:Status>
    </ord:GetOrderResponse>
  </soap:Body>
</soap:Envelope>
```

`Envelope` and `Body` belong to SOAP; `GetOrder`, `Id`, and `Status` belong to this application. An optional SOAP `Header` carries additional message information. SOAP also defines a `Fault` structure for reporting errors. This operation-based example is one usage pattern: SOAP can exchange documents without modeling remote function calls. The [W3C SOAP primer](https://www.w3.org/TR/soap12-part0/) explains these message structures and patterns.

SOAP services commonly describe their operations, message types, bindings, and endpoints in **WSDL** (Web Services Description Language), often with XML Schema for data types. WSDL is a separate specification, not a required element inside every SOAP message. See the [WSDL specification](https://www.w3.org/TR/wsdl.html).

### REST over HTTP: retrieve a resource representation

The order has a resource URL, and the HTTP method expresses the action:

```http
GET /orders/42 HTTP/1.1
Host: api.example.com
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "id": 42,
  "status": "shipped"
}
```

The JSON is a **representation** of the order. REST allows other formats, including XML and HTML. [Fielding's REST chapter](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_2_1)

HTTP already gives `GET` retrieval semantics. Other methods include `POST` for resource-specific processing, `PUT` for creating or replacing state at a target URI, and `DELETE` for requesting a resource's removal. Deletion need not erase the underlying stored data. Status codes communicate outcomes such as `201 Created` or `404 Not Found`. [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-9)

## Quick comparison

| Aspect | SOAP | REST over HTTP |
| --- | --- | --- |
| Defines | Message format and processing rules | Constraints on interactions |
| Example request | `GetOrder` message to `/OrderService` | `GET /orders/42` |
| Format | XML-based SOAP envelope | Representation format chosen by the API |
| Contract tooling | Commonly WSDL and XML Schema | Can use OpenAPI and schemas |
| Errors | SOAP `Fault`; HTTP status also matters when using HTTP | HTTP status plus an error representation |
| Transport | HTTP or another protocol with a SOAP binding | HTTP in this comparison |

SOAP is not restricted to HTTP; the [SOAP primer's protocol bindings](https://www.w3.org/TR/soap12-part0/) include an email example. REST itself does not mandate HTTP, though this note focuses on web APIs. [Fielding's connector view](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_3_2)

**REST can have a formal contract too.** [OpenAPI](https://spec.openapis.org/oas/v3.1.1.html) describes HTTP API operations, parameters, request and response schemas, and security schemes. Having an OpenAPI document does not establish REST conformance.

## What makes an API RESTful?

REST's constraints include client–server separation, stateless requests, cacheability, a uniform interface, layers, and optional code on demand. See [Fielding's original architectural definition](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1). Two details are easy to miss:

- **Stateless does not mean no database.** Orders remain stored on the server. Each request must be understandable without remembered client session context from earlier requests.
- **The uniform interface includes hypermedia:** links and controls in representations guide subsequent actions. JSON responses and noun-based URLs alone do not satisfy all REST constraints. The retrieval example above illustrates only part of the design. [Fielding's explanation of REST APIs and hypertext](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)

For HTTP APIs, a read using `GET` is safe and idempotent: it requests no state change, and repeating it has the same intended effect as making it once. The returned data can still change between reads. `PUT` and `DELETE` are idempotent but not safe; `POST` has no general idempotency guarantee. This distinction matters when retrying after a connection failure. [RFC 9110: common method properties](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2)

## Which should I use?

As a practical design recommendation, start with the integration requirements:

- **An existing partner exposes SOAP:** follow its WSDL and supported SOAP version. A JSON request will not satisfy that contract.
- **A new web or mobile API exposes resources:** a REST-oriented HTTP design is a useful starting point, with explicit schemas and documented HTTP behavior.
- **A requirement names a particular messaging extension:** check support for that extension in both client and server. SOAP's extensibility does not automatically provide security, reliable delivery, or transactions; those require additional mechanisms. [SOAP's scope and extensibility](https://www.w3.org/TR/soap12-part1/#intro)

Neither label guarantees better security or speed. Compare the actual authentication, authorization, payloads, caching, and implementation needed for the application.
