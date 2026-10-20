---
Title: SOAP vs. REST
Date: 2026-10-20 07:00
Category: Computer Science
Tags: cs, api, http, soap, rest, tech-notes
Slug: soap-vs-rest
Status: published
---

**SOAP is a messaging protocol; REST is an architectural style.** Both let applications communicate through APIs. SOAP standardizes message structure and processing. REST (Representational State Transfer) organizes interactions around resources and their representations. See the [SOAP specification](https://www.w3.org/TR/soap12-part1/) and [REST's original definition](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm).

## The same task, two interfaces

Imagine a shopping app asking for order `123`. These illustrative HTTPS exchanges omit routine headers.

### SOAP: send a structured message

A SOAP service might expose `GetOrder`. The client sends an XML message inside a standardized **SOAP 1.2 envelope**:

```http
POST /OrderService HTTP/1.1
Host: api.example.com
Content-Type: application/soap+xml; charset=utf-8

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
               xmlns:ord="https://example.com/orders">
  <soap:Body>
    <ord:GetOrder>
      <ord:Id>123</ord:Id>
    </ord:GetOrder>
  </soap:Body>
</soap:Envelope>
```

The server replies with another SOAP envelope containing the result or a `Fault`. `Envelope` and `Body` belong to SOAP; `GetOrder` belongs to this application. SOAP also supports document exchanges without remote function calls. [W3C SOAP primer](https://www.w3.org/TR/soap12-part0/)

### REST over HTTP: retrieve a resource representation

The order has a resource URL. The HTTP method expresses the action:

```http
GET /orders/123 HTTP/1.1
Host: api.example.com
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "id": 123,
  "status": "shipped"
}
```

The JSON is a **representation** of the order. A typical API could expose these actions:

```text
GET    /orders/123  → Read the order
POST   /orders      → Create an order
PATCH  /orders/123  → Update part of the order
DELETE /orders/123  → Delete the order
```

These routes apply standard [HTTP method semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-9), including [PATCH for partial modifications](https://www.rfc-editor.org/rfc/rfc5789.html). Creation is one use of `POST`; it also supports other resource-specific processing.

## Quick comparison

| Aspect | SOAP | REST over HTTP |
| --- | --- | --- |
| Format | XML-based envelope | Often JSON; other formats allowed |
| Typical interaction | Named operations or document messages | Resources accessed through HTTP methods |
| Interface description | Commonly [WSDL](https://www.w3.org/TR/wsdl.html) and XML Schema | Can use [OpenAPI](https://spec.openapis.org/oas/v3.1.1.html) and schemas |
| Transport | HTTP or another SOAP protocol binding | HTTP for web APIs |
| Complexity | Additional envelope and messaging machinery | Often simpler with standard HTTP tooling |

WSDL describes a service's operations, messages, and endpoints. OpenAPI can provide a formal contract for an HTTP API too. Neither description format guarantees a good API design.

## Useful distinctions

- **REST does not mean JSON.** XML, HTML, and other representations are possible.
- **Stateless does not mean no database.** Each request carries enough context to be understood independently; the server can still store orders. See [REST's constraints](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1).
- **REST includes more than resource URLs.** Its uniform interface includes links and controls that guide subsequent actions, called *hypermedia*. [Fielding's explanation](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)
- **SOAP is not inherently more secure.** Both can use HTTPS. SOAP also has [WS-Security](https://docs.oasis-open.org/wss/v1.1/wss-v1.1-spec-os-SOAPMessageSecurity.pdf), which supports signing and encrypting message content; this requires implementation and configuration.

## Which should I use?

As a practical starting point, consider REST for new web, mobile, and public APIs. Choose SOAP when an enterprise or partner integration requires its contract or messaging standards. Neither is universally better; compatibility and application requirements should drive the choice.
