#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequest,
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as hl from "@nktkas/hyperliquid";

import { ALL_MIDS_TOOL, CANDLE_SNAPSHOT_TOOL, L2_BOOK_TOOL } from "./tools.js";
import { getAllMids, getCandleSnapshot, getL2Book } from "./actions.js";

const DEFAULT_API_URL = "https://api.hyperliquid.xyz";
const ALLOWED_API_URLS = new Set([
  DEFAULT_API_URL,
  "https://api.hyperliquid-testnet.xyz",
]);

function resolveApiUrl(): string {
  const configured = process.env.HYPERLIQUID_API_URL?.trim();
  if (!configured) {
    return DEFAULT_API_URL;
  }
  if (!ALLOWED_API_URLS.has(configured)) {
    throw new Error(
      `HYPERLIQUID_API_URL must be one of: ${[...ALLOWED_API_URLS].join(", ")}`
    );
  }
  return configured;
}

async function main() {
  console.error("Starting Hyperliquid MCP server...");
  const server = new Server(
    {
      name: "hyperliquid",
      version: "0.0.1-vetted",
    },
    { capabilities: { tools: {} } }
  );

  const apiUrl = resolveApiUrl();
  console.error(`Using Hyperliquid API: ${apiUrl}`);

  const hyperliquidTransport = new hl.HttpTransport({ url: apiUrl });
  const hyperliquidClient = new hl.PublicClient({
    transport: hyperliquidTransport,
  });

  server.setRequestHandler(
    CallToolRequestSchema,
    async (request: CallToolRequest) => {
      const { name, arguments: args } = request.params;
      console.error(`CallToolRequest: ${name}`);

      try {
        switch (name) {
          case "get_l2_book": {
            if (!args) {
              throw new Error("No arguments provided");
            }
            return await getL2Book(hyperliquidClient, args);
          }
          case "get_all_mids": {
            return await getAllMids(hyperliquidClient);
          }
          case "get_candle_snapshot": {
            if (!args) {
              throw new Error("No arguments provided");
            }
            return await getCandleSnapshot(hyperliquidClient, args);
          }
          default:
            return {
              content: [{ type: "text", text: `Unknown tool: ${name}` }],
              isError: true,
            };
        }
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${
                error instanceof Error ? error.message : String(error)
              }`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    console.error("ListToolsRequest");
    return {
      tools: [ALL_MIDS_TOOL, CANDLE_SNAPSHOT_TOOL, L2_BOOK_TOOL],
    };
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Hyperliquid MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
