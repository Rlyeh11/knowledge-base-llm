# CORS 问题修复说明

## 问题描述

在本地运行时查询知识时，出现以下错误：

```
"OPTIONS /run HTTP/1.1" 405 Method Not Allowed
```

## 原因分析

这是一个 **CORS（跨域资源共享）** 预检请求失败的问题。

### 什么是 CORS？

CORS 是一种基于 HTTP 头的机制，允许服务器标示除了它自己以外的其他源（域、协议或端口），浏览器应该允许从这些源加载资源。

### 为什么会出现 OPTIONS 请求？

当浏览器从一个域（例如 `file://` 或 `http://localhost:3000`）向另一个域（例如 `http://localhost:5000`）发送请求时，如果满足以下条件，浏览器会先发送一个 **OPTIONS 预检请求**：

1. 使用了除 GET、POST、HEAD 之外的方法（如 PUT、DELETE）
2. 请求头中包含自定义字段
3. 请求头 `Content-Type` 不是 `application/x-www-form-urlencoded`、`multipart/form-data` 或 `text/plain`

预检请求的目的是询问服务器是否允许实际的跨域请求。

### 为什么返回 405 错误？

服务器没有正确处理 OPTIONS 方法，导致返回 "405 Method Not Allowed" 错误。

## 解决方案

在 `src/main.py` 中添加了 CORS 中间件配置：

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS 中间件 - 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)
```

### 配置说明

- `allow_origins=["*"]`: 允许所有来源的请求
  - **生产环境建议**: 修改为具体的域名列表，如 `["https://yourdomain.com"]`
- `allow_credentials=True`: 允许跨域请求携带凭证（如 cookies）
- `allow_methods=["*"]`: 允许所有 HTTP 方法（GET, POST, PUT, DELETE, OPTIONS 等）
- `allow_headers=["*"]`: 允许所有请求头

## 验证修复

重启服务后，应该可以正常工作：

```bash
# 停止当前服务（按 Ctrl+C）
# 重新启动
python src/main.py -m http -p 5000
```

现在浏览器发送 OPTIONS 请求时，服务器会返回正确的响应：

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
Access-Control-Allow-Credentials: true
```

## 生产环境安全建议

在生产环境中，应该限制 `allow_origins` 为特定的域名：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ],  # 仅允许特定域名
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # 限制允许的方法
    allow_headers=["Content-Type", "Authorization"],  # 限制允许的请求头
)
```

或者使用环境变量配置：

```python
import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 常见 CORS 问题

### 1. 预检请求失败

**症状**: 浏览器控制台显示 CORS 错误

**解决方案**: 确保 CORS 中间件正确配置，并且允许 OPTIONS 方法

### 2. 凭证问题

**症状**: 无法携带 cookies 或 authorization 头

**解决方案**:
- 设置 `allow_credentials=True`
- `allow_origins` 不能使用 `["*"]`，必须指定具体域名

### 3. 自定义请求头问题

**症状**: 自定义请求头被拒绝

**解决方案**: 在 `allow_headers` 中添加自定义头名称

## 测试 CORS

### 使用 curl 测试

```bash
# 测试 OPTIONS 预检请求
curl -X OPTIONS http://localhost:5000/run \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

# 预期响应头应包含：
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: *
# Access-Control-Allow-Headers: *
```

### 使用浏览器测试

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 发送请求
4. 查看 OPTIONS 请求的响应头

## 相关资源

- [MDN - CORS](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS)
- [FastAPI - CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [W3C - CORS 规范](https://www.w3.org/TR/cors/)

## 其他修复方式

如果你不想使用 CORS 中间件，还有以下替代方案：

### 1. 使用代理服务器

在前端和后端之间添加一个代理服务器，将请求转发到后端。

### 2. 使用 JSONP（已过时）

JSONP 是一种旧的技术，仅支持 GET 请求，现在不推荐使用。

### 3. 设置同源策略

确保前端和后端运行在同一域、同一端口下。

---

**注意**: CORS 中间件是解决跨域问题的推荐方案，配置简单且安全性好。
