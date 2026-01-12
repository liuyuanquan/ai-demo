# MCP Server 示例项目

这是一个使用 Model Context Protocol (MCP) SDK 创建的示例服务器项目，展示了如何注册和使用工具。

## 功能特性

- 使用 MCP SDK 创建服务器
- 注册和使用自定义工具
- 通过标准输入输出 (Stdio) 进行通信
- 支持工具调用和响应

## 安装

1. 克隆或下载项目文件
2. 安装依赖：

```bash
npm install
```

## 构建

构建项目：

```bash
npm run build
```

## 运行

### 运行服务器

```bash
npm start
```

### 运行客户端测试

```bash
npm test
```

## 工具说明

### 两数求和工具 (two_number_sum)

计算两个数字的和。

**参数：**
- `a` (number): 第一个数字
- `b` (number): 第二个数字

**返回值：**
- `content`: 包含计算结果的文本内容
- `structuredContent`: 包含计算结果的结构化数据

### 创建文件工具 (create_file)

创建一个新文件并写入指定内容。

**参数：**
- `fileName` (string): 文件名和路径
- `content` (string): 文件内容

**返回值：**
- `content`: 包含操作结果的文本内容
- `structuredContent`: 包含操作结果的结构化数据

## 代码结构

- `server.ts`: MCP 服务器实现
- `client.ts`: MCP 客户端测试实现
- `package.json`: 项目配置和依赖
- `tsconfig.json`: TypeScript 配置

## 使用示例

### 服务器端

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio';
import { z } from "zod";

// 创建 MCP Server 实例
const mcpServer = new McpServer(serverInfo, {
  capabilities: {
    tools: {}
  }
});

// 注册工具
mcpServer.registerTool(
  'tool_name',
  {
    description: "工具描述",
    inputSchema: {
      // 输入参数定义
    }
  },
  async (params, extra) => {
    // 工具实现
    return {
      content: [
        { type: 'text', text: "工具执行结果" }
      ],
      structuredContent: { result: "结构化结果" }
    };
  }
);

// 启动服务
async function startServer() {
  const transport = new StdioServerTransport();
  await mcpServer.connect(transport);
}

startServer();
```

### 客户端

```typescript
// 发送工具调用请求
const request = {
  jsonrpc: '2.0',
  id: 1,
  method: 'tools/call',
  params: {
    name: 'tool_name',
    arguments: {
      // 工具参数
    }
  }
};

// 发送请求并处理响应
```

## 协议说明

本项目使用 Model Context Protocol (MCP)，这是一个用于模型和服务器之间通信的协议。主要特点包括：

- JSON-RPC 2.0 基础
- 支持工具调用
- 支持资源管理
- 支持内容创建和编辑

## 依赖

- @modelcontextprotocol/sdk: MCP SDK
- zod: 数据验证库
- typescript: TypeScript 编译器

## 许可证

MIT
