# 知识库编译系统 - 使用指南

## 🚀 快速开始

### 方式一：本地部署（推荐）

#### 1. 启动服务

```bash
# 确保在项目根目录
python src/main.py -m http -p 5000
```

服务将在 `http://localhost:5000` 启动。

#### 2. 验证服务状态

```bash
curl http://localhost:5000/health
```

预期返回：
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

### 方式二：使用 Docker 部署

```bash
# 构建镜像
docker build -t knowledge-base .

# 运行容器
docker run -p 5000:5000 \
  -v $(pwd)/assets:/app/assets \
  knowledge-base
```

## 📡 API 使用说明

### 1. 摄取模式 - 添加新内容

**端点**: `POST /run`

**请求示例**:
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 知识管理最佳实践\n\n这里是内容...",
    "content_type": "markdown",
    "title": "知识管理最佳实践",
    "mode": "ingest"
  }'
```

**Python 示例**:
```python
import requests

response = requests.post(
    "http://localhost:5000/run",
    json={
        "content": "# 知识管理最佳实践\n\n这里是内容...",
        "content_type": "markdown",
        "title": "知识管理最佳实践",
        "mode": "ingest"
    }
)
print(response.json())
```

### 2. 问答模式 - 基于知识库回答问题

**端点**: `POST /run`

**请求示例**:
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "什么是知识库编译？",
    "mode": "qa"
  }'
```

**Python 示例**:
```python
import requests

response = requests.post(
    "http://localhost:5000/run",
    json={
        "question": "什么是知识库编译？",
        "mode": "qa"
    }
)
print(response.json())
```

### 3. 健康检查模式 - 检查知识库质量

**端点**: `POST /run`

**请求示例**:
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "health_check",
    "health_check_mode": "full"
  }'
```

**Python 示例**:
```python
import requests

response = requests.post(
    "http://localhost:5000/run",
    json={
        "mode": "health_check",
        "health_check_mode": "full"
    }
)
print(response.json())
```

## 🌐 Web 界面

如果你希望有一个可视化界面，可以使用以下简单的 HTML 页面：

创建一个文件 `index.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识库编译系统</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .section { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        h1, h2 { color: #333; }
        textarea { width: 100%; height: 150px; padding: 10px; margin: 10px 0; }
        input, select { width: 100%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        #result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>📚 知识库编译系统</h1>

    <!-- 摄取模式 -->
    <div class="section">
        <h2>📥 摄取新内容</h2>
        <textarea id="ingestContent" placeholder="输入你的内容（Markdown/HTML/纯文本）..."></textarea>
        <input type="text" id="ingestTitle" placeholder="文档标题（可选）">
        <select id="ingestType">
            <option value="markdown">Markdown</option>
            <option value="html">HTML</option>
            <option value="text">纯文本</option>
        </select>
        <button onclick="ingest()">摄取内容</button>
    </div>

    <!-- 问答模式 -->
    <div class="section">
        <h2>❓ 智能问答</h2>
        <input type="text" id="question" placeholder="输入你的问题...">
        <button onclick="askQuestion()">提问</button>
    </div>

    <!-- 健康检查模式 -->
    <div class="section">
        <h2>🏥 健康检查</h2>
        <select id="healthMode">
            <option value="full">完整检查</option>
            <option value="consistency">一致性检查</option>
            <option value="completeness">完整性检查</option>
            <option value="orphan">孤岛检查</option>
        </select>
        <button onclick="healthCheck()">执行检查</button>
    </div>

    <!-- 结果显示 -->
    <div id="result"></div>

    <script>
        const API_URL = 'http://localhost:5000/run';

        // 摄取内容
        async function ingest() {
            const content = document.getElementById('ingestContent').value;
            const title = document.getElementById('ingestTitle').value;
            const contentType = document.getElementById('ingestType').value;

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: content,
                    content_type: contentType,
                    title: title,
                    mode: 'ingest'
                })
            });

            const result = await response.json();
            displayResult('摄取结果', result);
        }

        // 提问
        async function askQuestion() {
            const question = document.getElementById('question').value;

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: question,
                    mode: 'qa'
                })
            });

            const result = await response.json();
            displayResult('问答结果', result);
        }

        // 健康检查
        async function healthCheck() {
            const mode = document.getElementById('healthMode').value;

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mode: 'health_check',
                    health_check_mode: mode
                })
            });

            const result = await response.json();
            displayResult('健康检查结果', result);
        }

        // 显示结果
        function displayResult(title, data) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<h3>${title}</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
        }
    </script>
</body>
</html>
```

然后在浏览器中打开 `index.html` 文件即可使用。

## 🔧 其他有用的 API

### 获取工作流参数定义

```bash
curl http://localhost:5000/graph_parameter
```

### 流式执行（适合长时间运行的任务）

```bash
curl -X POST http://localhost:5000/stream_run \
  -H "Content-Type: application/json" \
  -d '{
    "content": "你的内容...",
    "mode": "ingest"
  }'
```

### 取消正在运行的任务

```bash
curl -X POST http://localhost:5000/cancel/{run_id}
```

## 📂 查看生成的文件

所有生成的文件都存储在 `assets/knowledge_base/` 目录下：

```
assets/knowledge_base/
├── raw/articles/           # 原始内容
├── wiki/                   # 编译产物
│   ├── indexes/           # 索引文件
│   ├── summaries/         # 摘要
│   └── concepts/          # 概念条目
└── outputs/               # 输出文件
    ├── qa/                # 问答记录
    └── health/            # 健康检查报告
```

## 🔍 使用示例

### 示例1：摄取技术文档

```python
import requests

# 摄取技术文档
response = requests.post(
    "http://localhost:5000/run",
    json={
        "content": """
# Python 最佳实践

## 代码风格
- 使用 PEP 8 规范
- 编写清晰的注释
- 使用有意义的变量名

## 性能优化
- 避免不必要的循环
- 使用列表推导式
- 合理使用生成器
        """,
        "content_type": "markdown",
        "title": "Python 最佳实践",
        "mode": "ingest"
    }
)

print("摄取成功！")
```

### 示例2：智能问答

```python
import requests

# 提问
response = requests.post(
    "http://localhost:5000/run",
    json={
        "question": "Python 中如何优化代码性能？",
        "mode": "qa"
    }
)

result = response.json()
print(f"答案: {result['answer']}")
```

## 🚨 注意事项

1. **端口号**: 默认使用 5000 端口，如果端口被占用可以使用 `-p` 参数指定其他端口
2. **文件路径**: 所有文件路径都是相对于项目根目录的
3. **超时设置**: 默认超时时间为 15 分钟，可以在 `src/main.py` 中修改 `TIMEOUT_SECONDS` 常量
4. **数据持久化**: 所有数据保存在本地 `assets` 目录下，确保有足够的磁盘空间

## 🎯 高级用法

### OpenAI 兼容接口

如果你想使用支持 OpenAI API 的工具：

```bash
curl -X POST http://localhost:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "knowledge-base",
    "messages": [
      {"role": "user", "content": "什么是知识库编译？"}
    ]
  }'
```

### 执行单个节点

```bash
curl -X POST http://localhost:5000/node_run/summary \
  -H "Content-Type: application/json" \
  -d '{
    "raw_file_path": "assets/knowledge_base/raw/articles/xxx.md"
  }'
```

## 📞 故障排查

### 服务无法启动
- 检查端口 5000 是否被占用
- 确认 Python 环境和依赖包是否正确安装

### API 返回错误
- 检查请求格式是否正确
- 查看服务日志获取详细错误信息
- 确认文件路径和权限是否正确

### 文件未生成
- 检查 `assets` 目录是否有写权限
- 确认输入参数是否正确
- 查看服务日志了解详细情况
