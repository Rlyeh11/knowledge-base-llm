# 🚀 CORS 问题快速修复指南

## 问题描述

在本地运行时查询知识时，浏览器控制台显示：

```
Access to fetch at 'http://localhost:5000/run' from origin 'http://localhost:3000' has been blocked by CORS policy
Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource
```

或

```
"OPTIONS /run HTTP/1.1" 405 Method Not Allowed
```

## ⚡ 快速修复（3 步）

### 步骤 1: 确认修复已应用

系统已经内置了 CORS 配置，无需手动修改代码。确认 `src/main.py` 包含以下内容：

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 步骤 2: 重启服务

```bash
# 停止当前服务（按 Ctrl+C）

# 重新启动
python src/main.py -m http -p 5000
```

### 步骤 3: 验证修复

打开浏览器，再次尝试查询知识。问题应该已解决。

---

## 🧪 验证 CORS 配置

### 方法 1: 使用测试脚本（推荐）

```bash
# Linux/Mac
python test_cors.py

# Windows
test_cors.bat
```

预期输出：
```
✅ OPTIONS 预检请求
✅ POST 实际请求
✅ 复杂预检请求
🎉 所有测试通过！CORS 配置正确。
```

### 方法 2: 使用 curl 测试

```bash
curl -X OPTIONS http://localhost:5000/run \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

检查响应头是否包含：
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

### 方法 3: 使用浏览器开发者工具

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 发送请求
4. 查找 OPTIONS 请求，检查响应头

---

## 🔧 手动修复（如果需要）

如果步骤 1 中确认 CORS 配置不存在，请手动添加：

### 1. 编辑 `src/main.py`

在导入部分添加：
```python
from fastapi.middleware.cors import CORSMiddleware
```

在 `app = FastAPI()` 之后添加：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 重启服务

```bash
python src/main.py -m http -p 5000
```

---

## 📝 配置说明

### 开发环境配置（默认）

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)
```

### 生产环境配置（推荐）

```python
import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://yourdomain.com").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # 仅允许特定域名
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # 限制方法
    allow_headers=["Content-Type", "Authorization"],  # 限制请求头
)
```

---

## ❓ 常见问题

### Q1: 重启后仍然报错

**解决方案**:
1. 清除浏览器缓存（Ctrl+Shift+Delete）
2. 尝试无痕模式
3. 确认服务确实重启成功（查看日志）

### Q2: 使用不同端口时出错

**解决方案**:
CORS 配置中的 `allow_origins=["*"]` 允许所有来源，应该支持任何端口。如果仍出错，请检查：
- 服务是否正确启动
- 端口是否被正确监听

### Q3: 生产环境是否安全

**答案**: `allow_origins=["*"]` 在开发环境可以，但生产环境不安全。

**生产环境配置**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

### Q4: Docker 部署中的 CORS 问题

**解决方案**:
Docker 部署通常不会有 CORS 问题，因为前后端在同一网络中。如果遇到问题：
1. 确认 Docker 网络配置正确
2. 检查端口映射
3. 查看容器日志：`docker-compose logs knowledge-base`

---

## 📚 更多信息

- **详细文档**: [CORS_FIX.md](./CORS_FIX.md) - 完整的 CORS 问题分析
- **API 文档**: 访问 `http://localhost:5000/docs` 查看 FastAPI 自动生成的 API 文档
- **测试工具**: 使用 `test_cors.py` 自动化测试 CORS 配置

---

## 🎯 总结

- ✅ **问题原因**: 浏览器的 CORS 预检请求没有被正确处理
- ✅ **解决方案**: 已在代码中配置 CORS 中间件
- ✅ **修复步骤**: 重启服务即可生效
- ✅ **验证方法**: 使用 `test_cors.py` 测试脚本

---

**快速命令**:
```bash
# 重启服务
python src/main.py -m http -p 5000

# 测试 CORS
python test_cors.py
```
