import { useCallback, useEffect, useRef, useState } from "react";

export function useCamera() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [error, setError] = useState("");
  const [ready, setReady] = useState(false);

  const stop = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setReady(false);
  }, []);

  const start = useCallback(async () => {
    try {
      stop();
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "user",
          width: { ideal: 960 },
          height: { ideal: 720 },
        },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
        // Wait until the video is actually producing frames (mobile needs this)
        await new Promise<void>((resolve) => {
          const check = () => {
            if (videoRef.current && videoRef.current.videoWidth > 0) {
              resolve();
            } else {
              requestAnimationFrame(check);
            }
          };
          check();
        });
      }
      setReady(true);
      setError("");
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Camera permission failed.");
    }
  }, [stop]);

  useEffect(() => {
    void start();
    return stop;
  }, [start, stop]);

  return { videoRef, ready, error, start };
}

