---
title: "Socket Exception with HttpClient in C#"
date: 2024-01-15
tags: [csharp, dotnet, debugging]
description: "A deep dive into port exhaustion when creating and disposing HttpClient instances in .NET applications."
status: merged
---

## The Problem

If you've ever worked with `HttpClient` in C#, you might have encountered the infamous `SocketException` — usually when your application is under heavy load. The root cause? **Port exhaustion** from creating too many `HttpClient` instances.

```csharp
// DON'T do this — creates a new HttpClient per request
using (var client = new HttpClient())
{
    var response = await client.GetAsync("https://api.example.com/data");
}
```

Every time you `new` up an `HttpClient` and dispose it, the underlying TCP connection enters a `TIME_WAIT` state. Under high concurrency, you run out of available ports.

## The Solution

Use a **single shared instance** of `HttpClient`, or better yet, use `IHttpClientFactory` (available since .NET Core 2.1):

```csharp
// Register in Startup.cs / Program.cs
services.AddHttpClient("api", client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});
```

Then inject and use it:

```csharp
public class MyService
{
    private readonly HttpClient _client;

    public MyService(IHttpClientFactory factory)
    {
        _client = factory.CreateClient("api");
    }

    public async Task<string> GetDataAsync()
    {
        var response = await _client.GetAsync("/data");
        return await response.Content.ReadAsStringAsync();
    }
}
```

## Why IHttpClientFactory?

- **Manages handler lifetimes** — rotates `HttpMessageHandler` instances to avoid DNS issues
- **Prevents port exhaustion** — reuses connections from a pool
- **Supports Polly** — add retry policies, circuit breakers, etc.

## Key Takeaway

> Never `new` up `HttpClient` in a `using` block for repeated calls. Use `IHttpClientFactory` or a shared static instance.

This is one of those .NET gotchas that has bitten many production systems. The fix is simple once you know the pattern.
