import { useEffect, useMemo, useState } from "react";
import { fetchStickers } from "../api";
import type { Sticker } from "../types";

export function useStickers() {
  const [stickers, setStickers] = useState<Sticker[]>([]);
  const [selectedSticker, setSelectedSticker] = useState("sunglasses");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchStickers()
      .then((items) => {
        setStickers(items);
        if (items[0]) {
          setSelectedSticker(items[0].id);
        }
      })
      .catch((exc) => setError(exc instanceof Error ? exc.message : "Could not load stickers."));
  }, []);

  const activeSticker = useMemo(
    () => stickers.find((sticker) => sticker.id === selectedSticker),
    [selectedSticker, stickers]
  );

  return { activeSticker, error, selectedSticker, setSelectedSticker, stickers };
}

