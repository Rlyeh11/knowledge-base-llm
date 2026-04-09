# 🔑 SSH Key 配置指南

## ✅ SSH Key 已生成

你的 SSH key 已成功生成并配置！

## 📋 SSH Key 信息

### 公钥（需要添加到 GitHub）
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAf7XCWblt0B/G/4Dq2k5YcHNfAIaGyrWC9oXaBPJRzX knowledge-base-llm@github.com
```

### Key 信息
- **类型**: ED25519（更安全、更快）
- **注释**: knowledge-base-llm@github.com
- **指纹**: SHA256:5M/HVZ6zbdImXDEUwOQL6+gpt+zJLCmbgHUojw47fRo
- **私钥位置**: ~/.ssh/id_ed25519_knowledge_base
- **公钥位置**: ~/.ssh/id_ed25519_knowledge_base.pub
- **SSH 配置**: ~/.ssh/config

## 🚀 添加到 GitHub

### 步骤 1: 复制公钥

```bash
# 查看公钥
cat ~/.ssh/id_ed25519_knowledge_base.pub
```

**复制上面的完整公钥内容**（从 `ssh-ed25519` 开始到 `github.com` 结束）

### 步骤 2: 添加到 GitHub

1. 访问 GitHub SSH Keys 设置页面：
   - https://github.com/settings/keys

2. 点击 **New SSH key** 按钮

3. 填写信息：
   - **Title**: `knowledge-base-llm`（或任意描述名称）
   - **Key**: 粘贴刚才复制的公钥

4. 点击 **Add SSH key**

### 步骤 3: 验证连接

添加 SSH key 后，测试连接：

```bash
ssh -T git@github.com
```

如果成功，你会看到：
```
Hi Rlyeh11! You've successfully authenticated, but GitHub does not provide shell access.
```

## 🔧 配置说明

### SSH 配置文件
已自动创建 `~/.ssh/config` 文件，内容如下：

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_knowledge_base
    IdentitiesOnly yes
```

这个配置会：
- 自动使用生成的 SSH key
- 连接到 GitHub 时无需指定路径
- 提供更好的安全性

## 📝 推送代码

### 配置完成后，你可以直接推送代码：

```bash
# 设置上游分支并推送
git push -u main main

# 或简化为（设置上游后）
git push
```

### 如果仍然使用 HTTPS URL

如果你的仓库使用 HTTPS URL，可以改为 SSH URL：

```bash
# 查看当前远程 URL
git remote -v

# 改为 SSH URL
git remote set-url main git@github.com:Rlyeh11/knowledge-base-llm.git

# 验证
git remote -v
```

## ⚠️ 重要提示

### 安全建议

1. **不要泄露私钥**：
   - 私钥文件：`~/.ssh/id_ed25519_knowledge_base`
   - 永远不要分享或上传私钥

2. **定期更换**：
   - 如果怀疑私钥泄露，立即删除并重新生成
   - 从 GitHub 删除旧的 SSH key

3. **权限保护**：
   - 私钥权限：600（仅所有者可读写）
   - 公钥权限：644（所有者可读写，其他用户可读）

### 备份建议

```bash
# 备份 SSH key（安全的环境）
cp ~/.ssh/id_ed25519_knowledge_base ~/.ssh/id_ed25519_knowledge_base.backup
cp ~/.ssh/id_ed25519_knowledge_base.pub ~/.ssh/id_ed25519_knowledge_base.pub.backup
```

## 🔍 故障排查

### 问题 1: Permission denied (publickey)

**原因**: SSH key 还没有添加到 GitHub

**解决方案**:
1. 按照上面的步骤 1-3 添加 SSH key 到 GitHub
2. 等待 1-2 分钟让 GitHub 生效
3. 重新测试：`ssh -T git@github.com`

### 问题 2: Host key verification failed

**原因**: GitHub 的 host key 还没有添加

**解决方案**:
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

### 问题 3: 还是提示输入密码

**原因**: Git 使用 HTTPS URL 而不是 SSH URL

**解决方案**:
```bash
# 检查远程 URL
git remote -v

# 如果是 https://，改为 git@
git remote set-url main git@github.com:Rlyeh11/knowledge-base-llm.git
```

## 🎯 快速命令

### 常用命令

```bash
# 查看公钥
cat ~/.ssh/id_ed25519_knowledge_base.pub

# 测试连接
ssh -T git@github.com

# 查看远程配置
git remote -v

# 推送代码
git push -u main main

# 拉取代码
git pull main main
```

## 📚 相关资源

- [GitHub SSH Keys 文档](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)
- [生成 SSH Keys](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [排查 SSH 问题](https://docs.github.com/zh/authentication/troubleshooting-ssh)

---

## ✅ 完成清单

- [x] 生成 SSH key
- [x] 配置 SSH 客户端
- [x] 添加 GitHub host key
- [ ] 复制公钥到 GitHub
- [ ] 添加 SSH key 到 GitHub
- [ ] 测试 SSH 连接
- [ ] 推送代码

**下一步**: 将上面的公钥添加到 GitHub，然后测试连接！
