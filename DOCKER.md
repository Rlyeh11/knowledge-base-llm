# Docker 使用指南

## 快速开始

### 1. 使用 Docker 部署（推荐）

```bash
# 构建镜像
docker build -t knowledge-base .

# 运行容器
docker run -p 5000:5000 -v $(pwd)/assets:/app/assets knowledge-base

# 或使用 docker-compose（推荐）
docker-compose up -d
```

### 2. 验证部署

```bash
# 检查容器状态
docker-compose ps

# 查看日志
docker-compose logs -f knowledge-base

# 访问健康检查
curl http://localhost:5000/health
```

### 3. 使用客户端

```bash
# 进入容器
docker-compose exec knowledge-base bash

# 使用客户端
python client.py ingest "测试内容" --title "测试"

# 问答
python client.py qa "什么是知识库编译？"
```

### 4. 停止服务

```bash
# 停止容器
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷
docker-compose down -v
```

## 高级配置

### 自定义端口

```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "8080:5000"  # 使用 8080 端口

# 或使用命令行
docker run -p 8080:5000 knowledge-base
```

### 挂载本地目录

```bash
# 挂载整个项目目录
docker run -p 5000:5000 \
  -v $(pwd)/assets:/app/assets \
  -v $(pwd)/logs:/app/work/logs \
  knowledge-base
```

### 环境变量

```bash
# 使用环境变量配置
docker run -p 5000:5000 \
  -e LOG_LEVEL=DEBUG \
  -e MAX_WORKERS=4 \
  knowledge-base
```

## 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs knowledge-base

# 检查容器状态
docker ps -a

# 查看资源使用
docker stats knowledge-base
```

### 端口冲突

```bash
# 检查端口占用
lsof -i :5000

# 使用其他端口
docker run -p 5001:5000 knowledge-base
```

### 权限问题

```bash
# 设置正确的权限
chmod -R 755 assets
chmod -R 777 assets/knowledge_base
```

## 生产环境部署

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 使用 Systemd 管理服务

创建 `/etc/systemd/system/knowledge-base.service`:

```ini
[Unit]
Description=Knowledge Base System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/app/knowledge-base
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable knowledge-base
sudo systemctl start knowledge-base
sudo systemctl status knowledge-base
```

## 性能优化

### 资源限制

```yaml
# 在 docker-compose.yml 中添加
services:
  knowledge-base:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### 日志管理

```yaml
# 限制日志大小
services:
  knowledge-base:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 备份与恢复

### 备份数据

```bash
# 备份 assets 目录
tar -czf backup-$(date +%Y%m%d).tar.gz assets/

# 备份 Docker 卷
docker run --rm -v knowledge-base_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz /data
```

### 恢复数据

```bash
# 恢复 assets 目录
tar -xzf backup-20241201.tar.gz

# 恢复 Docker 卷
docker run --rm -v knowledge-base_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres-backup.tar.gz -C /
```

## 更新与升级

### 更新镜像

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build

# 重启服务
docker-compose up -d

# 查看更新状态
docker-compose logs -f knowledge-base
```

---

**注意：** Docker 部署是最推荐的部署方式，因为它可以避免本地环境配置问题，确保在各种操作系统上都能正常运行。
