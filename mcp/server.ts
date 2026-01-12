/**
 * MCP (Model Context Protocol) 服务器示例
 *
 * 这是一个基于 Model Context Protocol 的简单服务器实现，
 * 演示了如何注册和执行自定义工具，支持通过 stdio 进行通信。
 *
 * @module MCP Server
 * @version 1.0.0
 * @since 2026-01-12
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "node:fs";
import path from "node:path";

/**
 * 服务端信息配置
 */
const serverInfo = {
	name: "My MCP Server",
	description:
		"A simple MCP server demonstrating tool registration and execution",
	version: "1.0.0",
};

/**
 * 创建 MCP Server 实例
 *
 * @type {McpServer}
 * @description 配置 MCP 服务器，声明支持的能力
 */
const mcpServer = new McpServer(serverInfo, {
	capabilities: {
		tools: {}, // 声明支持工具调用能力
	},
});

/**
 * 注册 "两数求和" 工具
 *
 * @tool two_number_sum
 * @description 计算两个数字的和
 * @input {
 *   a: number, // 第一个数字
 *   b: number  // 第二个数字
 * }
 * @output {
 *   content: [{ type: 'text', text: string }],
 *   structuredContent: { result: number }
 * }
 */
mcpServer.registerTool(
	"two_number_sum",
	{
		description: "Calculate the sum of two numbers",
		inputSchema: {
			a: z.number().describe("First number"),
			b: z.number().describe("Second number"),
		},
	},
	async (params, extra) => {
		const { a, b } = params;
		// console.log(`Calculating sum of ${a} and ${b}`);
		const result = a + b;
		return {
			content: [
				{ type: "text", text: `The sum of ${a} and ${b} is ${result}` },
			],
			structuredContent: { result },
		};
	}
);

/**
 * 注册 "创建文件" 工具
 *
 * @tool create_file
 * @description 创建指定内容的新文件
 * @input {
 *   fileName: string, // 文件名（包含路径）
 *   content: string   // 文件内容
 * }
 * @output {
 *   content: [{ type: 'text', text: string }],
 *   structuredContent: {
 *     success: boolean,
 *     filePath?: string,
 *     error?: string
 *   }
 * }
 */
mcpServer.registerTool(
	"create_file",
	{
		description: "Create a new file with specified content",
		inputSchema: {
			fileName: z.string().describe("File name with path"),
			content: z.string().describe("File content"),
		},
	},
	async (input, extra) => {
		try {
			// console.log(`Creating file: ${input.fileName}`);
			const filePath = path.resolve(input.fileName);

			// 使用utf8编码写入文件，防止中文乱码
			fs.writeFileSync(filePath, input.content, "utf8");

			// console.log(`File created successfully: ${filePath}`);
			return {
				content: [
					{ type: "text", text: `File created successfully: ${filePath}` },
				],
				structuredContent: { success: true, filePath },
			};
		} catch (error) {
			console.error(`File create failed: ${error.message}`);
			return {
				content: [
					{ type: "text", text: `Failed to create file: ${error.message}` },
				],
				structuredContent: { success: false, error: error.message },
			};
		}
	}
);

/**
 * 启动 MCP 服务器
 *
 * @async
 * @function startServer
 * @description 初始化传输层并启动 MCP 服务器
 * @returns {Promise<void>}
 */
async function startServer() {
	try {
		// 创建标准输入输出传输层
		const transport = new StdioServerTransport();
		// console.log("MCP Server 启动中...");

		// 获取已注册的工具列表
		// const registeredTools = Object.keys(mcpServer["_registeredTools"]);
		// console.log("已注册工具:", registeredTools);

		// 连接传输层并启动服务
		await mcpServer.connect(transport);

		// console.log("✅ MCP Server 启动成功");
		// console.log("服务信息:", serverInfo);
	} catch (error) {
		console.error("❌ MCP Server 启动失败:", error);
	}
}

// 执行服务器启动
startServer();
