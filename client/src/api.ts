import type { AugmentResponse, Sticker } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:5001";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error ?? "Request failed.");
  }
  return payload as T;
}

export async function fetchStickers(): Promise<Sticker[]> {
  const payload = await request<{ stickers: Sticker[] }>("/api/stickers");
  return payload.stickers.map((sticker) => ({
    ...sticker,
    url: `${API_BASE_URL}${sticker.url}`,
  }));
}

export function augmentFrame(image: string, stickerId: string): Promise<AugmentResponse> {
  return request<AugmentResponse>("/api/augment", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image, stickerId }),
  });
}
