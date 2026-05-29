import { PublicClient } from "@nktkas/hyperliquid";

import { candleSnapshotSchema, l2BookSchema } from "./schemas.js";

export async function getL2Book(
  hyperliquidClient: PublicClient,
  args: unknown
) {
  const validatedArgs = l2BookSchema.parse(args);

  const l2Book = await hyperliquidClient.l2Book(validatedArgs);
  return {
    content: [{ type: "text", text: JSON.stringify(l2Book) }],
    isError: false,
  };
}

export async function getAllMids(hyperliquidClient: PublicClient) {
  const allMids = await hyperliquidClient.allMids();
  return {
    content: [{ type: "text", text: JSON.stringify(allMids) }],
    isError: false,
  };
}

export async function getCandleSnapshot(
  hyperliquidClient: PublicClient,
  args: unknown
) {
  const validatedArgs = candleSnapshotSchema.parse(args);
  const candleSnapshot = await hyperliquidClient.candleSnapshot(validatedArgs);
  return {
    content: [{ type: "text", text: JSON.stringify(candleSnapshot) }],
    isError: false,
  };
}
