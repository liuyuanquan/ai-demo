/**
 * MCP (Model Context Protocol) 客户端示例
 *
 * 这是一个基于 Model Context Protocol 的简单客户端实现，
 * 演示了如何通过 stdio 与 MCP 服务器通信并执行工具调用。
 *
 * @module MCP Client
 * @version 1.0.0
 * @since 2026-01-12
 */

import { spawn } from "child_process";
import type {
	JSONRPCRequest,
	JSONRPCResponse,
} from "@modelcontextprotocol/sdk/types.js";

/**
 * 启动 MCP 服务端子进程
 *
 * @type {ChildProcessWithoutNullStreams}
 * @description 创建并管理与 MCP 服务器的子进程通信
 */
const mcpServerProcess = spawn("node", ["./dist/server.js"]);

/**
 * 监听服务端标准输出响应
 *
 * @description 处理服务端返回的数据，区分 JSON 响应和普通日志
 * @param {Buffer} data - 服务端输出的原始数据
 */
mcpServerProcess.stdout.on("data", (data: Buffer) => {
	const resStr: string = data.toString().trim();
	if (resStr) {
		try {
			console.log("\n⬅️ 服务端响应：", JSON.parse(resStr) as JSONRPCResponse);
		} catch (e) {
			console.log("\n📌 服务端日志：", resStr);
		}
	}
});

/**
 * 监听服务端标准错误输出
 *
 * @description 处理服务端产生的错误信息
 * @param {Buffer} err - 服务端输出的错误数据
 */
mcpServerProcess.stderr.on("data", (err: Buffer) => {
	console.error("\n❌ 服务端错误：", err.toString());
});

/**
 * 测试请求列表
 *
 * @type {JSONRPCRequest[]}
 * @description 遵循 MCP/JSON-RPC 2.0 协议的测试请求集合
 */
const requests: JSONRPCRequest[] = [
	// 1. 初始化握手请求（必须第一个发送）
	{
		jsonrpc: "2.0",
		id: 1,
		method: "initialize",
		params: {
			protocolVersion: "2024-11-05",
			capabilities: {
				roots: { listChanged: true, sampling: {}, elicitation: {} },
			},
			clientInfo: {
				name: "test-client",
				title: "Test Client",
				version: "1.0.0",
			},
		},
	},
	// 2. 调用两数求和工具
	{
		jsonrpc: "2.0",
		id: 2,
		method: "tools/call",
		params: {
			name: "two_number_sum",
			arguments: { a: 100, b: 200 },
		},
	},
	// 3. 调用创建文件工具
	{
		jsonrpc: "2.0",
		id: 3,
		method: "tools/call",
		params: {
			name: "create_file",
			arguments: {
				fileName: "stdio-mcp-file.txt",
				content: "通过StdioServerTransport创建的MCP测试文件",
			},
		},
	},
];

/**
 * 发送测试请求
 *
 * @description 按顺序发送测试请求，间隔1秒
 */
requests.forEach((req: JSONRPCRequest, index: number) => {
	setTimeout(() => {
		const reqJson: string = JSON.stringify(req);
		console.log(`\n➡️ 发送请求 ${index + 1}: ${req.method}`);
		mcpServerProcess.stdin.write(reqJson + "\n");
	}, index * 1000);
});

/**
 * 优雅关闭连接
 *
 * @description 所有请求发送完成后，关闭标准输入流
 */
setTimeout(() => {
	mcpServerProcess.stdin.end();
	console.log("\n✅ 所有请求发送完成！");
}, requests.length * 1000 + 500);
