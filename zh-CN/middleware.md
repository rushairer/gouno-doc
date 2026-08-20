# 中间件

[English](../middleware.md)

## 内置与推荐中间件

gouno 及项目模板提供了以下核心中间件组件：

### 1. 异常恢复（Recovery）

从 panic 中平滑恢复，记录堆栈日志并返回 HTTP 500（`NewInternalServerErrorResponse`）。

```go
middleware.RecoveryMiddleware()
```

### 2. 安全响应头（Security Headers）

统一注入浏览器安全响应头（包括 `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, HSTS 以及自定义 CSP / Permissions-Policy）。

```go
gounoMiddleware.SecurityHeaders(gounoMiddleware.SecurityHeadersOptions{
    IsProduction:      !globalConfig.WebServerConfig.Debug,
    PermissionsPolicy: "geolocation=(), camera=(), microphone=(), payment=()",
    CSP:               "default-src 'self'; ...",
})
```

### 3. 请求超时（Timeout）

当请求处理耗时超过配置时返回 HTTP 408（`NewRequestTimeoutResponse`）。

```go
middleware.TimeoutMiddleware(globalConfig.WebServerConfig.RequestTimeout)
```

### 4. 频率限制（RateLimit）

基于客户端 IP 的滑动窗口限流器，具备防止内存膨胀的 `maxVisitors` 容量保护。超限时返回 HTTP 429 及 `Retry-After` 头。

```go
gounoMiddleware.RateLimitMiddleware(ctx, limit, window)

// 示例：每分钟 120 次请求
gounoMiddleware.RateLimitMiddleware(ctx, 120, time.Minute)
```

每次请求的响应头：

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 119
X-RateLimit-Reset: 2026-08-20T12:00:00Z
```

### 5. CSRF 防护

`gouno/middleware` 提供了标准的双重 Cookie 提交（Double-Submit Cookie）CSRF 防护工具：

```go
// 在处理函数或中间件中设置/校验
err := gounoMiddleware.EnsureCSRFCookie(ctx, "csrf_token", isSecure, 24*time.Hour)
matches := gounoMiddleware.CSRFMatches(cookieToken, submittedToken)
```

### 6. OIDC RS256 令牌校验器

`gouno/auth` 提供了线程安全的 OIDC JWKS 验签器（后台静默拉取并自动缓存）：

```go
verifier := auth.NewVerifier("https://auth.example.com/.well-known/jwks.json")
claims, err := verifier.Verify(tokenString, auth.Options{
    Issuer:   "https://auth.example.com",
    Audience: "my-service",
})
```

---

## 服务端流水线配置

在 `cmd/gouno/web.go` 中：

```go
engine := gin.New()
engine.Use(
    gin.Logger(),
    middleware.RecoveryMiddleware(),
    middleware.SecurityHeadersMiddleware(!globalConfig.WebServerConfig.Debug),
    middleware.TimeoutMiddleware(globalConfig.WebServerConfig.RequestTimeout),
    gounoMiddleware.RateLimitMiddleware(ctx, globalConfig.WebServerConfig.RateLimitPerMinute, time.Minute),
    // 在此挂载你的业务中间件
)
```

---

## 编写自定义中间件

标准 Gin 中间件模式，配合 `gouno.New*Response()` 不可变工厂方法输出响应：

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

