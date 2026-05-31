# 配置管理

[English](../configuration.md)

gouno 使用 [Viper](https://github.com/spf13/viper) 进行多环境 YAML 配置管理。

## 配置文件

```
config/
├── development.yaml    ← 本地开发
├── test.yaml           ← CI/测试环境
├── production.yaml     ← 生产环境（敏感信息用环境变量）
├── config.go           ← 结构体定义
└── config_manager.go   ← 线程安全加载器
```

## 环境选择

```bash
./bin/my-service web -e development    # 使用 config/development.yaml
./bin/my-service web -e test           # 使用 config/test.yaml
./bin/my-service web -e production     # 使用 config/production.yaml
```

## 配置结构

```yaml
web_server:
    address: 0.0.0.0
    port: 8080
    debug: false
    idle_timeout: 60s
    read_timeout: 5s
    write_timeout: 30s
    request_timeout: 10s
    rate_limit_per_minute: 120

database:
    default: postgres
    drivers:
        postgres:
            name: postgres
            driver: pgx
            dsn: host=localhost user=app password=secret dbname=app port=5432

redis:
    dsn: redis://localhost:6379
    max_active_conns: 6000

log:
    level: 0    # -1: Debug, 0: Info, 1: Warn, 2: Error, 3: DPanic, 4: Panic, 5: Fatal
```

## 环境变量覆盖

所有配置项都可以通过 `GOUNO_` 前缀的环境变量覆盖：

```bash
# 覆盖 web_server.port
GOUNO_WEB_SERVER_PORT=3000 ./bin/my-service web

# 覆盖 database.drivers.postgres.dsn
GOUNO_DATABASE_DRIVERS_POSTGRES_DSN="host=db user=app ..." ./bin/my-service web
```

## 优先级

```
CLI 参数 (--port) > 环境变量 (GOUNO_*) > 配置文件 > 默认值
```

## 代码中访问配置

```go
configManager := config.NewConfigManager(cmd, configPath, env)
cfg := configManager.Config()

fmt.Println(cfg.WebServerConfig.Port)          // "8080"
fmt.Println(cfg.DatabaseConfig.GetDefaultDriver().DSN)
```
