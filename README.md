# Tuta 邮箱自动登录工具

一个通过 GitHub Actions 定期自动登录 Tuta 邮箱的工具，防止账户因不活跃被回收。支持多账户管理，配置完成后无需维护，让您的 Tuta 邮箱保持永久活跃状态。

## 项目描述

Tuta 邮箱（原 Tutanota）会在账户六个月不活跃后将其回收，这对于那些作为备用或安全用途而不经常登录的账户是一个潜在风险。

Tuta Email 自动登录工具是一个专为 Tuta 邮箱用户设计的自动化解决方案，旨在解决长期不活跃账户可能被回收的问题。

本工具通过 GitHub Actions 提供的自动化能力，定期模拟用户登录操作，确保您的 Tuta 邮箱账户始终保持活跃状态。

只需简单配置后，系统会按照预设的时间表（默认每月两次）自动完成登录过程并记录结果，让您安心使用 Tuta 邮箱而不必担心账户被回收。

## 特性

- 📅 自动定期登录：每月 1 日和 15 日自动运行
- 🔄 支持多账号：可同时管理任意数量的 Tuta 邮箱账户
- 📝 登录记录：自动生成并保存登录历史记录
- 🔒 安全可靠：账户凭据存储在 GitHub Secrets 中
- 🛠️ 可手动触发：需要时可手动运行工作流

## 快速开始

### 1. Fork 本仓库

点击 GitHub 界面右上角的 "Fork" 按钮，将本仓库复制到您的 GitHub 账户下。

### 2. 配置 GitHub Secrets

1. 在您 fork 的仓库中，点击 "Settings" 选项卡
2. 在左侧边栏中选择 "Secrets and variables" > "Actions"
3. 点击 "New repository secret" 按钮添加您的邮箱凭据

对于第一个账号，添加以下 secrets：
- `TUTA_EMAIL`: 您的 Tuta 邮箱地址
- `TUTA_PASSWORD`: 您的 Tuta 邮箱密码

对于更多账号，按照以下格式添加（将 N 替换为递增的数字）：
- `TUTA_EMAIL_N`: 第 N 个 Tuta 邮箱地址
- `TUTA_PASSWORD_N`: 第 N 个 Tuta 邮箱密码

例如：
```
TUTA_EMAIL    // 第一个账号
TUTA_PASSWORD // 第一个账号密码

TUTA_EMAIL_2    // 第二个账号
TUTA_PASSWORD_2 // 第二个账号密码

TUTA_EMAIL_3    // 第三个账号
TUTA_PASSWORD_3 // 第三个账号密码

... 以此类推
```

### 3. 启用 GitHub Actions

1. 在您 fork 的仓库中，点击 "Actions" 选项卡
2. 如果 Actions 被禁用，会有提示询问您是否启用，点击 "I understand my workflows, go ahead and enable them"
3. 在工作流列表中选择 "Tuta 邮箱自动登录"
4. 点击 "Enable workflow" 按钮

## 手动运行

如果您想立即测试或手动触发登录流程：

1. 进入您仓库的 "Actions" 选项卡
2. 选择左侧的 "Tuta 邮箱自动登录" 工作流
3. 点击 "Run workflow" 按钮
4. 在弹出的下拉菜单中保持默认分支选择，然后点击绿色的 "Run workflow" 按钮

## 查看结果

每次工作流运行后，系统会自动更新 `login_history.log` 文件，记录每个账号的登录结果。您可以在仓库中查看此文件，了解登录历史情况。

## 工作原理

此工具使用 Selenium 自动化工具控制 Chrome 浏览器，模拟真实用户登录 Tuta 邮箱的过程。GitHub Actions 按计划定期运行此自动化脚本，确保您的邮箱保持活跃状态。

脚本会自动：
1. 启动无头浏览器
2. 访问 Tuta 登录页面
3. 填写邮箱和密码
4. 完成登录过程
5. 验证登录状态
6. 记录结果

## 常见问题

### Q: 如何修改登录频率？
A: 编辑 `.github/workflows/login.yml` 文件中的 `cron` 表达式。默认设置为每月 1 日和 15 日的 UTC 时间 00:00 运行。

### Q: 脚本登录失败怎么办？
A: 检查您提供的邮箱和密码是否正确。如果仍有问题，可以查看 Actions 日志以获取详细错误信息，或提交 Issue 寻求帮助。

### Q: 添加新账号后需要修改代码吗？
A: 不需要。只要按照上述格式在 GitHub Secrets 中添加新的账号凭据，脚本会自动检测并处理。

### Q: 我的账号凭据安全吗？
A: 您的账号凭据存储在 GitHub Secrets 中，该机制专为存储敏感信息而设计，不会在日志或仓库代码中显示。

## 贡献

欢迎提交 Pull Request 或 Issue 来改进此工具。如果您有任何问题或建议，请随时联系。

## 许可

本项目采用 Unlicense 许可，这意味着它被发布到公共领域。您可以自由使用、修改、分发和执行本软件的工作，无需任何归属或通知。详情请查看 [LICENSE](LICENSE) 文件。

---

**免责声明**：此工具仅用于帮助用户维持邮箱活跃状态，请勿用于任何违反 Tuta 服务条款的行为。作者不保证本工具可用性，也不对任何滥用此工具造成的后果负责。

