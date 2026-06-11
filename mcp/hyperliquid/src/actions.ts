import { PublicClient } from "@nktkas/hyperliquid";

import {
  candleSnapshotSchema,
  getMidSchema,
  l2BookSchema,
} from "./schemas.js";

function findSimilarSymbols(allMids: Record<string, string>, symbol: string) {
  const query = symbol.toUpperCase();
  return Object.keys(allMids)
    .filter((key) => {
      const upper = key.toUpperCase();
      return upper.includes(query) || query.includes(upper);
    })
    .slice(0, 10);
}

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

export async function getMid(hyperliquidClient: PublicClient, args: unknown) {
  const { symbol } = getMidSchema.parse(args);
  const allMids = await hyperliquidClient.allMids();
  const exact = allMids[symbol];

  if (exact !== undefined) {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ symbol, mid: exact }),
        },
      ],
      isError: false,
    };
  }

  const upperMatch = Object.entries(allMids).find(
    ([key]) => key.toUpperCase() === symbol.toUpperCase()
  );
  if (upperMatch) {
    const [matchedSymbol, mid] = upperMatch;
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ symbol: matchedSymbol, mid }),
        },
      ],
      isError: false,
    };
  }

  const similar = findSimilarSymbols(allMids, symbol);
  const suffix =
    similar.length > 0
      ? ` Similar symbols: ${similar.join(", ")}.`
      : " No similar symbols found.";
  throw new Error(`Symbol '${symbol}' is not listed on Hyperliquid.${suffix}`);
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
