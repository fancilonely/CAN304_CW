# CAN304_CW

## Project Overview

This repository contains the code and supporting materials for the CAN304 coursework project.  
The project focuses on a lightweight prototype for **secure text transmission with context-aware validation**, developed to demonstrate the design, implementation, and testing process of the coursework.

The current prototype is based on the project topic:

**Dynamic Watermarking for Secure Information Transmission**

In this project, the term *watermark* does not refer to a traditional multimedia watermark embedded in images or audio. Instead, it is implemented as a **dynamic context-bound logical token** used to control whether a message is still valid under the intended receiving conditions.

---

## Project Objectives

The current prototype aims to demonstrate the following core ideas:

- **Plaintext protection**  
  Ensure that unauthorized parties cannot directly read the original plaintext during transmission.

- **Dynamic watermark token**  
  Generate a unique token for each message to improve security and flexibility.

- **Context binding**  
  Bind the token to metadata such as sender, receiver, timestamp, and message ID.

- **One-time usage constraint**  
  Ensure that a valid message becomes invalid after its first successful authorized use.

- **Anomaly detection**  
  Detect message tampering, token mismatch, metadata mismatch, replay, and reuse.

- **Lightweight implementation**  
  Keep the prototype simple and feasible within the coursework scope.

---

## Current Prototype Scope

The current version implements a **minimum viable prototype (MVP)** for secure text transmission.  
Its workflow can be summarized as follows:

1. The sender inputs a plaintext message.
2. The system encrypts the message into ciphertext.
3. The system generates:
   - a dynamic watermark token
   - an integrity tag
   - a one-time usage constraint
4. The sender outputs a package containing only ciphertext and verification-related information.
5. The receiver verifies the package step by step.
6. The receiver returns either:
   - **ACCEPT** if all checks pass
   - **REJECT** if any check fails

This means a message is **not accepted simply because it can be decrypted**.  
It is accepted only when it is decrypted under the correct context and has not already been consumed.

---

## Repository Structure

```text
CAN304_CW/
├─ app.py
├─ config.py
├─ crypto_utils.py
├─ sender.py
├─ receiver.py
├─ storage.py
├─ test_scenarios.py
├─ requirements.txt
├─ README.md
└─ .gitignore

# CAN304_CW
## 项目概述
此存储库包含了 CAN304 课程作业项目的代码及相关辅助材料。
该项目旨在开发一个轻量级的原型，用于实现具有上下文感知验证功能的**安全文本传输**，旨在展示该课程作业的设计、实现和测试过程。
当前的原型是基于以下项目主题开发的：
**动态水印技术在安全信息传输中的应用**
在该项目中，“水印”这一术语并非指嵌入在图像或音频中的传统多媒体水印。而是被设计成一种“动态的、与上下文相关的逻辑标记”，用于控制消息在预期接收条件下的有效性。
---

## 项目目标
当前的原型旨在展示以下核心理念：
- **明文保护**
确保在传输过程中，未经授权的人员无法直接读取原始明文内容。
- **动态水印令牌**
为每条消息生成一个独特的令牌，以增强安全性并提高灵活性。
- **上下文绑定**
将令牌与诸如发送方、接收方、时间戳和消息 ID 等元数据进行绑定。
- “一次性使用限制”
确保有效消息在首次成功获得授权使用后即失效。
- **异常检测**
检测消息篡改、令牌不匹配、元数据不匹配、重放以及重复使用情况。
- **轻量级实现**
在课程范围内保持原型设计简洁且可行。
---

## 当前原型范围
当前版本实现了用于安全文本传输的“最小可行原型”（MVP）。
其工作流程可概括如下：
1. 发送方输入一份明文信息。2. 该系统将消息加密为密文。3. 该系统生成以下内容：
- 一个动态水印令牌
- 一个完整性标签
- 一次性的使用限制4. 发送方输出一个仅包含密文和相关验证信息的包裹。5. 收件人会逐步检查包裹。6. 接收方会做出如下两种回应：
- 如果所有检查都通过，则回复“接受”；
- 如果有任何一项检查未通过，则回复“拒绝”。
这意味着一条信息不会仅仅因为能够被解密就被接受。
只有在正确的情境下解密后且尚未被使用过的情况下，这条信息才会被接受。
---

## 存储库结构
CAN304_CW/
├─ app.py
├─ config.py
├─ crypto_utils.py
├─ sender.py
├─ receiver.py
├─ storage.py
├─ test_scenarios.py
├─ requirements.txt
├─ README.md
└─ .gitignore