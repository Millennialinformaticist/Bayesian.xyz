import { Tool } from "@modelcontextprotocol/sdk/types.js";

export const ALL_MIDS_TOOL: Tool = {
  name: "get_all_mids",
  description: "Get mid prices for all coins on Hyperliquid",
  inputSchema: {
    type: "object",
    properties: {},
    required: [],
  },
};

export const CANDLE_SNAPSHOT_TOOL: Tool = {
  name: "get_candle_snapshot",
  description: "Get candlestick data for a token on Hyperliquid",
  inputSchema: {
    type: "object",
    properties: {
      coin: {
        type: "string",
        description: "The symbol of the token to get candlestick data for",
      },
      interval: {
        type: "string",
        description: "Time interval (e.g., '15m', '1h')",
      },
      startTime: {
        type: "number",
        description: "Start time in milliseconds since epoch",
      },
      endTime: {
        type: "number",
        description: "End time in milliseconds since epoch (optional)",
      },
    },
    required: ["coin", "interval", "startTime"],
  },
};

export const L2_BOOK_TOOL: Tool = {
  name: "get_l2_book",
  description: "Get the L2 book of a token on Hyperliquid",
  inputSchema: {
    type: "object",
    properties: {
      symbol: {
        type: "string",
        description: "The symbol of the token to get the L2 book for",
      },
    },
    required: ["symbol"],
  },
};
