# CAN304_CW

## 项目未来方向

### 代码层
- 保留当前这套 core prototype
- 保持 SQLite 持久化
- 支持 package 导出 / 加载
- 保留自动 demo flow
- 保留 validation scenarios

### 展示层
- 一页 architecture diagram
- 一页 package structure
- 一页 validation result table
- 一页 discussion / limitations

### 可选加分层
- 一个简单的 Tkinter 小界面  
  或者
- 一个更好看的 CLI + 文件导入导出

---

## 项目概述

本仓库为 CAN304 课程作业项目的代码仓库，用于展示课程设计过程中的分析、实现与测试结果。

当前项目主题为：

**Dynamic Watermarking for Secure Information Transmission**  
**信息传输安全中的动态水印原型**

需要说明的是，本项目中的“watermark”并不是传统意义上嵌入图像、音频或视频中的多媒体水印，而是实现为一种**动态的、与上下文绑定的逻辑令牌（logical token）**，用于控制消息是否仍然在预期接收条件下有效。

本项目当前实现的是一个**轻量级原型（lightweight prototype）**，重点不在于构建完整的工业级安全通信平台，而在于验证以下核心思想是否能够被清晰实现并正确运行：

- 消息在传输中以密文形式存在
- 每条消息具有独立的动态 token
- token 与上下文信息绑定
- 消息在首次合法使用后失效
- 接收端能够识别篡改、上下文不匹配和重放 / 重复使用行为

---

## 项目目标

当前原型旨在展示以下核心目标：

- **明文保护（Plaintext Protection）**  
  确保未经授权的第三方无法在传输过程中直接读取原始明文。

- **动态水印令牌（Dynamic Watermark Token）**  
  为每条消息生成一个独立的动态 token，以提高安全性和灵活性。

- **上下文绑定（Context Binding）**  
  将 token 与发送者、接收者、时间戳、消息 ID 等上下文信息绑定。

- **一次性使用约束（One-Time Usage Constraint）**  
  确保一条消息在第一次成功授权使用后即被视为已消费，后续再次提交将被拒绝。

- **异常检测（Anomaly Detection）**  
  检测消息篡改、token 不匹配、metadata 不匹配、重放和重复使用行为。

- **轻量级实现（Lightweight Implementation）**  
  保持系统结构简洁，便于在 CAN304 课程范围内实现、演示和扩展。

---

## 当前原型范围

当前版本实现了一个用于安全文本传输的**最小可行原型（MVP）**。

其核心流程如下：

1. 发送端输入明文消息
2. 系统将明文加密为密文（ciphertext）
3. 系统生成：
   - 动态 watermark token
   - integrity tag（完整性标签）
   - one-time usage state（一次性使用状态）
4. 发送端输出一个 package，其中仅包含密文和相关验证信息，不包含明文
5. 接收端逐步执行验证
6. 系统返回：
   - **ACCEPT**：所有检查通过
   - **REJECT**：任一检查失败

这意味着：

**消息不会仅仅因为“可以解密”就被接受，而只有在正确上下文下、且未被消费过时才会被接受。**

---

## 当前版本特性

当前版本已经实现以下功能：

- 使用 AES-GCM 对消息进行加密与解密
- 为每条消息生成动态 context-bound token
- 对 package 核心字段生成 integrity tag
- 在接收端执行完整验证流程
- 支持 one-time usage 检测
- 支持 replay / reuse rejection
- 提供交互式菜单演示
- 提供一键自动完整演示流程
- 提供正式测试场景输出

---

## 运行方式

### 推荐环境

- Python 3.14
- Visual Studio Code
- `venv` 虚拟环境

### 安装依赖

```bash
pip install -r requirements.txt