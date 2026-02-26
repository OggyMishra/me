---
title: "C# 6.0 Features That Changed How I Write Code"
date: 2024-03-05
tags: [csharp, dotnet, language-features]
description: "A look at the C# 6.0 features that had the biggest impact on everyday coding — from string interpolation to expression-bodied members."
status: merged
---

## Why C# 6.0 Still Matters

Even though C# has moved well past version 6.0, the features introduced in that release fundamentally changed how C# code *looks and feels*. These aren't flashy features — they're the kind of quality-of-life improvements that you use in nearly every file.

## String Interpolation

Before:

```csharp
string message = string.Format("Hello, {0}! You have {1} messages.", name, count);
```

After:

```csharp
string message = $"Hello, {name}! You have {count} messages.";
```

Cleaner, more readable, and less error-prone. No more counting format placeholders.

## Null-Conditional Operator

```csharp
// Before: verbose null checks
string name = null;
if (person != null && person.Address != null)
    name = person.Address.City;

// After: concise chaining
string name = person?.Address?.City;
```

This single operator eliminated thousands of lines of null-checking boilerplate across codebases.

## Expression-Bodied Members

For simple methods and properties, expression bodies reduce ceremony:

```csharp
// Property
public string FullName => $"{FirstName} {LastName}";

// Method
public override string ToString() => $"{Name} ({Age})";
```

## nameof Operator

```csharp
// Before: magic strings that break during refactoring
throw new ArgumentNullException("name");

// After: refactor-safe
throw new ArgumentNullException(nameof(name));
```

## The Bigger Picture

These features share a common theme: **reducing ceremony**. C# 6.0 made the language more expressive without adding complexity. Every feature feels natural once you start using it, and going back to code without them feels painful.

Modern C# (10, 11, 12) has continued this trend with records, pattern matching, and file-scoped namespaces — but C# 6.0 was the turning point that made C# feel *modern*.
