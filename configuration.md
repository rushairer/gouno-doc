# Configuration

[中文](./zh-CN/configuration.md)

gouno uses [Viper](https://github.com/spf13/viper) for multi-environment YAML configuration.

## Config Files

```
config/
├── development.yaml    ← Local development
├── test.yaml           ← CI/test environment
├── production.yaml     ← Production (use env vars for secrets)
├── config.go           ← Struct definitions
└── config_manager.go   ← Thread-safe loader
```

## Environment Selection

```bash
./bin/my-service web -e development    # Uses config/development.yaml
./bin/my-service web -e test           # Uses config/test.yaml
./bin/my-service web -e production     # Uses config/production.yaml
```

## Config Structure

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

## Environment Variable Override

All config values can be overridden with environment variables using the `GOUNO_` prefix:

```bash
# Override web_server.port
GOUNO_WEB_SERVER_PORT=3000 ./bin/my-service web

# Override database.drivers.postgres.dsn
GOUNO_DATABASE_DRIVERS_POSTGRES_DSN="host=db user=app ..." ./bin/my-service web
```

## Priority

```
CLI flag (--port) > Environment variable (GOUNO_*) > Config file > Default
```

## Access Config in Code

```go
configManager := config.NewConfigManager(cmd, configPath, env)
cfg := configManager.Config()

fmt.Println(cfg.WebServerConfig.Port)          // "8080"
fmt.Println(cfg.DatabaseConfig.GetDefaultDriver().DSN)
```
