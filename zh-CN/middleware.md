# 中间件

[English](../middleware.md)

## 内置中间件

gouno 提供三个中间件，按以下顺序执行：

### 1. Recovery

从 panic 中恢复，返回 HTTP 500。

```go
middleware.RecoveryMiddleware()
```

### 2. Timeout

请求超过配置时长时返回 HTTP 408。

```go
middleware.TimeoutMiddleware(config.RequestTimeout)
```

### 3. RateLimit

基于 IP 的滑动窗口限流器。超限时返回 HTTP 429 及 `Retry-After` 头。

```go
gounoMiddleware.RateLimitMiddleware(ctx, limit, window)
// 示例：每分钟 120 次请求
gounoMiddleware.RateLimitMiddleware(ctx, 120, time.Minute)
```

每次请求的响应头：

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 119
X-RateLimit-Reset: 2026-05-31T12:00:00Z
```

## 添加自定义中间件

在 `cmd/gouno/web.go` 中：

```go
engine.Use(
    gin.Logger(),
    middleware.RecoveryMiddleware(),
    middleware.TimeoutMiddleware(globalConfig.WebServerConfig.RequestTimeout),
    gounoMiddleware.RateLimitMiddleware(ctx, globalConfig.WebServerConfig.RateLimitPerMinute, time.Minute),
    // 你的中间件
    myAuthMiddleware(),
    myCORSMiddleware(),
)
```

## 编写自定义中间件

标准 Gin 中间件模式：

```go
func MyMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // 请求前
        start := time.Now()

        c.Next()

        // 请求后
        duration := time.Since(start)
        log.Printf("%s %s 耗时 %v", c.Request.Method, c.Request.URL.Path, duration)
    }
}
```

中断请求：

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
