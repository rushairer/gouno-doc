# Middleware

[中文](./zh-CN/middleware.md)

## Built-in & Recommended Middleware

gouno and its template scaffold provide the following core middleware components:

### 1. Recovery

Recovers from panics, logs stack traces, and returns HTTP 500 (`NewInternalServerErrorResponse`).

```go
middleware.RecoveryMiddleware()
```

### 2. Security Headers

Sets standard browser security response headers (e.g. `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, HSTS, and custom CSP/Permissions-Policy).

```go
gounoMiddleware.SecurityHeaders(gounoMiddleware.SecurityHeadersOptions{
    IsProduction:      !globalConfig.WebServerConfig.Debug,
    PermissionsPolicy: "geolocation=(), camera=(), microphone=(), payment=()",
    CSP:               "default-src 'self'; ...",
})
```

### 3. Timeout

Returns HTTP 408 (`NewRequestTimeoutResponse`) if request processing exceeds the configured duration.

```go
middleware.TimeoutMiddleware(globalConfig.WebServerConfig.RequestTimeout)
```

### 4. RateLimit

IP-based sliding window rate limiter with map size protection (`maxVisitors`). Returns HTTP 429 with `Retry-After` header when exceeded.

```go
gounoMiddleware.RateLimitMiddleware(ctx, limit, window)

// Example: 120 requests per minute
gounoMiddleware.RateLimitMiddleware(ctx, 120, time.Minute)
```

Response headers on every request:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 119
X-RateLimit-Reset: 2026-08-20T12:00:00Z
```

### 5. CSRF Protection

`gouno/middleware` provides secure double-submit CSRF utilities:

```go
// In handlers or middleware
err := gounoMiddleware.EnsureCSRFCookie(ctx, "csrf_token", isSecure, 24*time.Hour)
matches := gounoMiddleware.CSRFMatches(cookieToken, submittedToken)
```

### 6. OIDC RS256 Token Verifier

`gouno/auth` provides a thread-safe JWKS verifier with background caching:

```go
verifier := auth.NewVerifier("https://auth.example.com/.well-known/jwks.json")
claims, err := verifier.Verify(tokenString, auth.Options{
    Issuer:   "https://auth.example.com",
    Audience: "my-service",
})
```

---

## Server Pipeline Configuration

In `cmd/gouno/web.go`:

```go
engine := gin.New()
engine.Use(
    gin.Logger(),
    middleware.RecoveryMiddleware(),
    middleware.SecurityHeadersMiddleware(!globalConfig.WebServerConfig.Debug),
    middleware.TimeoutMiddleware(globalConfig.WebServerConfig.RequestTimeout),
    gounoMiddleware.RateLimitMiddleware(ctx, globalConfig.WebServerConfig.RateLimitPerMinute, time.Minute),
    // Your custom middleware here
)
```

---

## Writing Custom Middleware

Standard Gin middleware pattern using immutable `gouno.New*Response()` factories:

```go
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.JSON(http.StatusUnauthorized, gouno.NewUnauthorizedResponse())
            c.Abort()
            return
        }
        c.Next()
    }
}
```

