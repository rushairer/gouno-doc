# Middleware

[中文](./zh-CN/middleware.md)

## Built-in Middleware

gouno provides three middleware components applied in this order:

### 1. Recovery

Recovers from panics and returns HTTP 500.

```go
middleware.RecoveryMiddleware()
```

### 2. Timeout

Returns HTTP 408 if a request exceeds the configured duration.

```go
middleware.TimeoutMiddleware(config.RequestTimeout)
```

### 3. RateLimit

IP-based sliding window rate limiter. Returns HTTP 429 with `Retry-After` header when exceeded.

```go
gounoMiddleware.RateLimitMiddleware(ctx, limit, window)
// Example: 120 requests per minute
gounoMiddleware.RateLimitMiddleware(ctx, 120, time.Minute)
```

Response headers on every request:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 119
X-RateLimit-Reset: 2026-05-31T12:00:00Z
```

## Add Custom Middleware

In `cmd/gouno/web.go`:

```go
engine.Use(
    gin.Logger(),
    middleware.RecoveryMiddleware(),
    middleware.TimeoutMiddleware(globalConfig.WebServerConfig.RequestTimeout),
    gounoMiddleware.RateLimitMiddleware(ctx, globalConfig.WebServerConfig.RateLimitPerMinute, time.Minute),
    // Your middleware here
    myAuthMiddleware(),
    myCORSMiddleware(),
)
```

## Write Custom Middleware

Standard Gin middleware pattern:

```go
func MyMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Before request
        start := time.Now()

        c.Next()

        // After request
        duration := time.Since(start)
        log.Printf("%s %s took %v", c.Request.Method, c.Request.URL.Path, duration)
    }
}
```

To abort the request:

```go
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.JSON(http.StatusUnauthorized, gouno.UnauthorizedResponse)
            c.Abort()
            return
        }
        c.Next()
    }
}
```
