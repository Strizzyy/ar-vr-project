import { useRef, useState } from "react";
import { CameraStage } from "./components/CameraStage";
import { ControlPanel } from "./components/ControlPanel";
import { useAugmentedStream } from "./hooks/useAugmentedStream";
import { useCamera } from "./hooks/useCamera";
import { useStickers } from "./hooks/useStickers";

export function App() {
  const { videoRef, ready, error: cameraError, start } = useCamera();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const { activeSticker, error: stickerError, selectedSticker, setSelectedSticker, stickers } = useStickers();
  const [isLive, setIsLive] = useState(true);
  const { augmentedImage, faceCount, status } = useAugmentedStream({
    canvasRef,
    enabled: isLive,
    ready,
    selectedSticker,
    videoRef,
  });

  return (
    <main className="app-shell">
      <CameraStage augmentedImage={augmentedImage} canvasRef={canvasRef} videoRef={videoRef} />
      <ControlPanel
        activeSticker={activeSticker}
        cameraError={cameraError}
        faceCount={faceCount}
        isLive={isLive}
        onRestartCamera={() => void start()}
        onSelectSticker={setSelectedSticker}
        onToggleLive={() => setIsLive((value) => !value)}
        selectedSticker={selectedSticker}
        status={status}
        stickerError={stickerError}
        stickers={stickers}
      />
    </main>
  );
}
