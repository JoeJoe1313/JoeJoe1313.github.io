---
Title: API Requests vs. MCP
Date: 2026-11-16 07:00
Category: Computer Science
Tags: cs, api, http, mcp, ai, tech-notes
Slug: api-requests-vs-mcp
Status: published
---

**Direct API requests call a service through its own interface. MCP gives AI applications a shared protocol for discovering and using tools and context.** The Model Context Protocol can sit in front of an existing API, so one workflow can use both. See the [MCP architecture overview](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture).

Here, *API requests* means direct calls to an HTTP API. API is a broader term: libraries, REST services, and RPC interfaces all expose APIs, and MCP itself defines a programmatic interface.

## The same task, two interfaces

Imagine looking up order `123`. The following examples are illustrative; the HTTP exchange omits authentication and routine headers.

### Direct API: call the order endpoint

The application knows the service's URL, parameters, and response format:

```http
GET /orders/123 HTTP/1.1
Host: api.example.com
Accept: application/json
```

```json
{
  "id": 123,
  "status": "shipped"
}
```

That knowledge can come from documentation, an SDK, or an [OpenAPI description](https://spec.openapis.org/oas/v3.1.1.html). Direct APIs can have machine-readable schemas too.

### MCP: discover and call an order tool

An AI application is the **host**. Its **MCP client** communicates with an **MCP server**, which exposes capabilities. The client can request `tools/list` and receive a tool definition such as:

```json
{
  "name": "get_order",
  "description": "Retrieve an order's shipping status by its ID.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "order_id": { "type": "integer" }
    },
    "required": ["order_id"],
    "additionalProperties": false
  }
}
```

The host can present this definition to a model. If the model proposes using the tool, the host controls execution and its client sends a `tools/call` request. These are the application-specific parameters, excluding protocol metadata and the JSON-RPC envelope:

```json
{
  "name": "get_order",
  "arguments": { "order_id": 123 }
}
```

`tools/list` and `tools/call` are standardized MCP methods; `get_order` and `order_id` belong to this server. The server executes the tool and returns an MCP result containing text, structured data, or other supported content. [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)

For this example, the tool implementation could make the same `GET /orders/123` request:

```text
AI host → MCP client → MCP server → Orders API
```

It could also query a database directly. MCP standardizes the interaction with the tool; the server still implements the actual lookup.

## Quick comparison

| Aspect | Direct HTTP API requests | MCP |
| --- | --- | --- |
| Discovering operations | Service documentation, SDKs, or OpenAPI | Standard discovery methods such as `tools/list` |
| Calling an operation | The service's HTTP methods, URLs, and payloads | JSON-RPC methods such as `tools/call` |
| Contract | Defined by each service | Shared protocol, with server-specific tool names and schemas |
| Reuse | Integrate each service's contract into your application | Expose a server to compatible MCP hosts |
| Operational cost | Manage the API integration | Also manage the MCP integration; a remote wrapper can add a network hop |

MCP messages can travel over **stdio** for a local subprocess or **Streamable HTTP** for an HTTP connection. An MCP call can therefore itself be an HTTP request. [MCP transport specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)

## What MCP adds, and what remains your responsibility

MCP also defines **resources** for contextual data and **prompts** for reusable message templates. Servers can expose the features they need. Authentication, access controls, and decisions about which actions to allow still require implementation; a tool schema does not establish permission to access an order. [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)

A model can use a direct API through a function your application supplies, so AI tool use does not require MCP. MCP's value is a reusable integration protocol across compatible applications. It does not choose tools, guarantee correct arguments, or automatically manage conversation memory.

## Which should I use?

As a practical starting point, use **direct API requests** for a known workflow in a web app, backend, or script, especially when you need close control over requests and latency. Consider **MCP** when several AI applications should discover and use the same tools or data through a common interface. Existing APIs can continue serving ordinary clients while an MCP server exposes selected capabilities to AI hosts.
