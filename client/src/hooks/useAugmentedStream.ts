import { RefObject, useEffect, useRef, useState } from "react";
import { augmentFrame } from "../api";
import { captureVideoFrame } from "../utils/captureFrame";

const PROCESS_INTERVAL_MS = 180;

type UseAugmentedStreamOptions = {
  canvasRef: RefObject<HTMLCanvasElement | null>;
  enabled: boolean;
  ready: boolean;
  selectedSticker: string;
  videoRef: RefObject<HTMLVideoElement | null>;
};

export function useAugmentedStream({
  canvasRef,
  enabled,
  ready,
  selectedSticker,
  videoRef,
}: UseAugmentedStreamOptions) {
  const busyRef = useRef(false);
  const [augmentedImage, setAugmentedImage] = useState("");
  const [faceCount, setFaceCount] = useState(0);
  const [status, setStatus] = useState("Starting camera");

  useEffect(() => {
    if (!ready || !enabled) {
      return;
    }

    const timer = window.setInterval(async () => {
      if (busyRef.current || !videoRef.current || !canvasRef.current) {
        return;
      }

      const frame = captureVideoFrame(videoRef.current, canvasRef.current);
      if (!frame) {
        return;
      }

      busyRef.current = true;
      try {
        const result = await augmentFrame(frame, selectedSticker);
        setAugmentedImage(result.image);
        setFaceCount(result.faces.length);
        setStatus(result.faces.length ? "Sticker locked" : "Looking for a face");
      } catch (exc) {
        setStatus(exc instanceof Error ? exc.message : "AR request failed.");
      } finally {
        busyRef.current = false;
      }
    }, PROCESS_INTERVAL_MS);

    return () => window.clearInterval(timer);
  }, [canvasRef, enabled, ready, selectedSticker, videoRef]);

  return { augmentedImage, faceCount, status };
}
